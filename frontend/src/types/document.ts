export interface Document {
  id: string;
  filename: string;
  file_size: number;
  mime_type: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  created_at: string;
  summary?: string;
  extracted_text?: string;
}
