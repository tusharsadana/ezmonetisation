// wrapper for axios
import axios from "axios";
import * as _ from "lodash";


const axiosAPI = axios.create({
    baseURL: 'localhost:8000/api/',
});

const postRequest = async (url, body, headers = null) => {

    if (!_.isNull(headers)) {

    }
    else {
        headers = {}
    }
}

const getRequest = async (url, headers) => { }


const putRequest = async (url, body, headers) => { }

const deleteRequest = async (url, headers) => { }

const apiService = {
    postRequest,
    getRequest,
    putRequest,
    deleteRequest
}

export default apiService;