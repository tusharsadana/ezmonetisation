import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from "react-toastify";
import 'react-toastify/dist/ReactToastify.css';
import CancelIcon from '@mui/icons-material/Cancel';

const TransactionCancelledPage: React.FC = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const redirectTimeout = setTimeout(() => {
      navigate('/plans');
    }, 3000);

    return () => {
      clearTimeout(redirectTimeout);
      toast.error('Transaction Cancelled');
    };
  }, [navigate]);

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <CancelIcon style={{ fontSize: '5rem', color: '#FF0000' }} />
      <h1 style={{ color: '#FF0000' }}>Transaction Cancelled</h1>
    </div>
  );
};

export default TransactionCancelledPage;
