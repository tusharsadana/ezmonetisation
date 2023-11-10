# stdlib
import json
import logging

# thirdparty
from sqlalchemy import text

# project
from src.monetization_service.core.db import get_session_cm

logger = logging.getLogger(__name__)


async def run_query():
    async with get_session_cm() as session:
        result = await session.execute(
            text(
                """
                with model_info as (select document.id,
                           json_object_agg(
                                   model_version.model_type,
                                   json_build_object(
                                           'version',
                                           model_version.version,
                                           'is_current',
                                           model_version.is_current
                                       )
                               ) as model_info
                    from document
                             join document_model_version
                                  on document_model_version.document_id =
                                     document.id
                             join model_version
                                  on document_model_version.model_version_id =
                                     model_version.id
                    where document.file_status = 4
                    group by document.id),
     entity_values as (select entity_type.id,
                              json_agg(
                                      json_build_object(
                                              'normalized_text',
                                              entity.normalized_text,
                                              'score_initial',
                                              entity.score_initial,
                                              'disabled',
                                              entity_type.disabled,
                                              'confirmed',
                                              entity.confirmed,
                                              'manual',
                                              entity.manual
                                          )
                                  ) as entity_values
                       from entity_type
                                join entity
                                     on entity.entity_type_id = entity_type.id
                                join document
                                     on entity_type.document_id = document.id
                       where document.file_status = 4
                       group by entity_type.id),
     entities as (select document.id document_id,
                         json_object_agg(
                                 entity_type.name,
                                 entity_values.entity_values
                             ) as    entity_types
                  from document
                           join entity_type
                                on entity_type.document_id = document.id
                           join entity_values
                                on entity_values.id = entity_type.id
                  where document.file_status = 4
                  group by document.id)
select document.id document_id,
       entities.entity_types,
       model_info.model_info
from document
         join entities on entities.document_id = document.id
         join model_info on model_info.id = document.id
where document.file_status = 4 and
  document.modified_at > now() - INTERVAL '1 DAY'
    order by document.modified_at
                """
            )
        )
    for res in result.all():
        doc_id = str(res[0])
        entities = json.dumps(res[1])
        model_info = json.dumps(res[2])
        logger.info(
            "Verification service query result for doc_id"
            " %s - entities: %s, model_info: %s"
            % (doc_id, entities, model_info)
        )

    # log number of docs reviewed
    for day in (1, 7, 31):
        result = await session.execute(
            text(
                """
                select
                    count(*) number_of_docs,
                    count(distinct document.user_email) number_of_users,
                    count(*) / count(distinct document.user_email) average_doc_per_user
                from document
                where document.modified_at > now() - INTERVAL '%s DAY'
                """
                % day
            )
        )
        result = result.all()
        logger.info(
            "Number of docs reviewed for last %s days:"
            " %s - number_of_docs, "
            "%s - number_of_users, "
            "%s - average_doc_per_user"
            % (day, result[0][0], result[0][1], result[0][2])
        )
    # log number of docs edited and not edited
    result = await session.execute(
        text(
            """
            WITH max_score_entities AS
     (SELECT entity_type.name          AS name,
             entity_type.id            AS id,
             max(entity.score_initial) AS score_initial
      FROM entity_type
               JOIN entity ON entity_type.id = entity.entity_type_id
               JOIN document ON entity_type.document_id = document.id
      WHERE document.file_status =4
        AND entity_type.name not IN ('Document Type', 'Currency')
        AND entity.manual IS false
      GROUP BY entity_type.id, entity_type.name),
 all_confirmed_disabled_entities AS
     (SELECT entity_type.name                 AS name,
             entity_type.document_id          AS document_id,
             entity.manual                    AS manual,
             entity_type.disabled             AS disabled,
             entity.confirmed                 AS confirmed,
             max_score_entities.score_initial AS score_initial,
             entity_type.document_id          AS document_id__1
      FROM entity_type
               JOIN entity ON entity_type.id = entity.entity_type_id
               JOIN document ON entity_type.document_id = document.id
               LEFT OUTER JOIN max_score_entities
                               ON max_score_entities.name =
                                  entity_type.name AND
                                  max_score_entities.id =
                                  entity_type.id AND
                                  max_score_entities.score_initial =
                                  entity.score_initial
      WHERE document.file_status = 4
        AND entity_type.name not IN ('Document Type', 'Currency')
        AND (entity_type.disabled IS true OR entity.confirmed)),
doc_entities as (select all_confirmed_disabled_entities.document_id,
   count(CASE
             WHEN (all_confirmed_disabled_entities.confirmed IS true AND
                   all_confirmed_disabled_entities.manual IS false AND
                   all_confirmed_disabled_entities.score_initial IS NOT NULL)
                 THEN 1 END)                                             AS not_edited,
   count(CASE
             WHEN (all_confirmed_disabled_entities.confirmed IS true AND
                   all_confirmed_disabled_entities.manual IS false AND
                   all_confirmed_disabled_entities.score_initial IS NULL)
                 THEN 1 END)                                             AS edited,
   count(DISTINCT CASE
                      WHEN (all_confirmed_disabled_entities.disabled IS true)
                          THEN all_confirmed_disabled_entities.document_id END) AS disabled,
   count(CASE
             WHEN (all_confirmed_disabled_entities.confirmed IS true AND
                   all_confirmed_disabled_entities.manual IS true)
                 THEN 1 END)                                             AS manual
FROM all_confirmed_disabled_entities
GROUP BY all_confirmed_disabled_entities.document_id),
doc_edited as (select doc_entities.document_id,
   case
       when (doc_entities.edited > 0 or doc_entities.disabled > 0 or doc_entities.manual > 0)
       then 1
         else 0
         end as doc_edited
from doc_entities)
select count(case when doc_edited.doc_edited = 1 then 1 end) docs_with_edits,
count(case when doc_edited.doc_edited = 0 then 1 end) docs_without_edits
from doc_edited

            """
        )
    )
    result = result.all()
    logger.info(
        "Number of docs with edits:"
        " %s, "
        "without edits - %s" % (result[0][0], result[0][1])
    )
