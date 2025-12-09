'use client';

import React, { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import { useSession } from 'next-auth/react';
import { Document } from '@/types/document';
import { FileText, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export function DocumentList({ refreshTrigger }: { refreshTrigger: number }) {
  const { data: session } = useSession();
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchDocuments = useCallback(async () => {
    if (!session?.accessToken) return;
    try {
      const res = await axios.get(`${API_URL}/api/v1/documents/`, {
        headers: { Authorization: `Bearer ${session.accessToken}` },
      });
      setDocuments(res.data);
    } catch (error) {
      console.error('Failed to fetch documents', error);
    } finally {
      setLoading(false);
    }
  }, [session?.accessToken]);

  useEffect(() => {
    fetchDocuments();
  }, [fetchDocuments, refreshTrigger]);

  // Polling for status updates if any doc is pending/processing
  useEffect(() => {
    if (!documents.some(d => d.status === 'pending' || d.status === 'processing')) return;
    
    const interval = setInterval(fetchDocuments, 5000);
    return () => clearInterval(interval);
  }, [documents, fetchDocuments]);

  if (loading) {
    return <div className="text-center py-4 text-gray-500">Loading documents...</div>;
  }

  if (documents.length === 0) {
    return <div className="text-center py-8 text-gray-500 bg-gray-50 rounded-lg border border-dashed border-gray-300">No documents uploaded yet.</div>;
  }

  return (
    <div className="space-y-3">
      {documents.map((doc) => (
        <div key={doc.id} className="flex items-center justify-between p-4 bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-shadow">
          <div className="flex items-center space-x-3">
            <div className={`p-2 rounded-full ${getStatusColor(doc.status)}`}>
               <FileText className="w-5 h-5 text-gray-700" />
            </div>
            <div>
              <p className="font-medium text-gray-900">{doc.filename}</p>
              <p className="text-xs text-gray-500">
                {(doc.file_size / 1024 / 1024).toFixed(2)} MB • {new Date(doc.created_at).toLocaleDateString()}
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <StatusBadge status={doc.status} />
          </div>
        </div>
      ))}
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  switch (status) {
    case 'completed':
      return (
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
          <CheckCircle className="w-3 h-3 mr-1" /> Ready
        </span>
      );
    case 'failed':
      return (
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
          <AlertCircle className="w-3 h-3 mr-1" /> Failed
        </span>
      );
    case 'processing':
    case 'pending':
    default:
      return (
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
          <Loader2 className="w-3 h-3 mr-1 animate-spin" /> Processing
        </span>
      );
  }
}

function getStatusColor(status: string) {
    switch (status) {
        case 'completed': return 'bg-green-100';
        case 'failed': return 'bg-red-100';
        default: return 'bg-yellow-100';
    }
}
