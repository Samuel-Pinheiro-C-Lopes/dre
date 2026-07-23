import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { extractRules } from '../services/api';
import { useRuleStore } from '../services/state';
import { RuleForm } from '../components/RuleForm';
import { UploadCloud, Loader2, AlertCircle } from 'lucide-react';

export const RuleExtractorPage: React.FC = () => {
  const { setRules, loading, setLoading } = useRuleStore();
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;
    const file = acceptedFiles[0];
    
    setLoading(true);
    setError(null);
    try {
      const data = await extractRules(file);
      setRules(data.rules);
    } catch (err: any) {
      setError(err.message || 'An error occurred during extraction. Is the backend running?');
    } finally {
      setLoading(false);
    }
  }, [setRules, setLoading]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ 
    onDrop,
    multiple: false
  });

  return (
    <div className="page-container">
      <header className="page-header">
        <div className="logo-container">
          <div className="logo-icon">AI</div>
          <h1>Rule Extractor</h1>
        </div>
        <p>Upload a document (.pdf, .docx, .txt) and let AI extract the core rules automatically.</p>
      </header>

      <div className="content-grid">
        <section className="upload-section glass-panel">
          <div 
            {...getRootProps()} 
            className={`dropzone ${isDragActive ? 'active' : ''} ${loading ? 'loading' : ''}`}
          >
            <input {...getInputProps()} />
            {loading ? (
              <div className="dropzone-content">
                <Loader2 className="spinner icon-primary" size={64} />
                <h3>Analyzing Document...</h3>
                <p>Please wait while the AI extracts rules.</p>
              </div>
            ) : (
              <div className="dropzone-content">
                <UploadCloud className="icon-primary" size={64} />
                <h3>{isDragActive ? "Drop document here" : "Upload Document"}</h3>
                <p>Drag & drop a file here, or click to browse</p>
                <span className="file-types">Supports: PDF, DOCX, TXT</span>
              </div>
            )}
          </div>
          {error && (
            <div className="error-message">
              <AlertCircle size={20} />
              <span>{error}</span>
            </div>
          )}
        </section>

        <section className="rules-section">
          <h2>Extracted Rules</h2>
          <RuleForm />
        </section>
      </div>
    </div>
  );
};
