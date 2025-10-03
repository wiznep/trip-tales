  
  import React, { useState, useCallback } from 'react';
import { Upload, Video, Image, X, FileVideo, Film } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';

interface UploadedFile {
  id: string;
  file: File;
  preview?: string;
  type: 'video' | 'image';
}

interface UploadZoneProps {
  onFilesUpload: (files: UploadedFile[]) => void;
  uploadedFiles: UploadedFile[];
}

export const UploadZone: React.FC<UploadZoneProps> = ({ onFilesUpload, uploadedFiles }) => {
  const [isDragOver, setIsDragOver] = useState(false);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    
    const files = Array.from(e.dataTransfer.files);
    processFiles(files);
  }, []);

  const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    processFiles(files);
  }, []);

  const processFiles = useCallback((files: File[]) => {
    const validFiles = files.filter(file => 
      file.type.startsWith('video/') || file.type.startsWith('image/')
    );

    const uploadedFiles: UploadedFile[] = validFiles.map(file => ({
      id: Math.random().toString(36).substr(2, 9),
      file,
      type: file.type.startsWith('video/') ? 'video' : 'image',
      preview: file.type.startsWith('image/') ? URL.createObjectURL(file) : undefined
    }));

    onFilesUpload(uploadedFiles);
  }, [onFilesUpload]);

  const removeFile = useCallback((id: string) => {
    const updatedFiles = uploadedFiles.filter(file => file.id !== id);
    onFilesUpload(updatedFiles);
  }, [uploadedFiles, onFilesUpload]);

  return (
    <Card className="relative overflow-hidden bg-card/50 backdrop-blur-sm border-border/50">
      <div
        className={`
          relative p-8 border-2 border-dashed rounded-lg transition-all duration-300
          ${isDragOver 
            ? 'border-primary bg-primary/5 shadow-upload' 
            : 'border-border hover:border-primary/50 hover:bg-card/80'
          }
        `}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <input
          type="file"
          id="file-upload"
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          multiple
          accept="video/*,image/*"
          onChange={handleFileSelect}
        />
        
        <div className="text-center space-y-4">
          <div className="relative mx-auto w-16 h-16">
            <Upload className={`
              w-16 h-16 mx-auto text-primary transition-all duration-300
              ${isDragOver ? 'scale-110 animate-bounce' : 'animate-float'}
            `} />
          </div>
          
          <div>
            <h3 className="text-xl font-semibold text-foreground mb-2">
              Drop your travel memories here
            </h3>
            <p className="text-muted-foreground">
              Upload videos and images from your trip. Supports MP4, MOV, JPG, PNG
            </p>
          </div>
          
          <Button 
            variant="gradient" 
            className="hover:scale-105 transition-transform duration-300"
          >
            <FileVideo className="w-4 h-4 mr-2" />
            Choose Files
          </Button>
        </div>
      </div>

      {uploadedFiles.length > 0 && (
        <div className="p-6 border-t border-border/50">
          <h4 className="text-lg font-medium text-foreground mb-4 flex items-center">
            <Film className="w-5 h-5 mr-2 text-primary" />
            Uploaded Files ({uploadedFiles.length})
          </h4>
          
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {uploadedFiles.map((file) => (
              <div key={file.id} className="relative group">
                <div className="aspect-video bg-muted rounded-lg overflow-hidden border border-border/50">
                  {file.type === 'image' && file.preview ? (
                    <img 
                      src={file.preview} 
                      alt={file.file.name}
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center">
                      <Video className="w-8 h-8 text-muted-foreground" />
                    </div>
                  )}
                </div>
                
                <Button
                  size="sm"
                  variant="destructive"
                  className="absolute -top-2 -right-2 w-6 h-6 rounded-full p-0 opacity-0 group-hover:opacity-100 transition-opacity duration-200"
                  onClick={() => removeFile(file.id)}
                >
                  <X className="w-3 h-3" />
                </Button>
                
                <p className="text-xs text-muted-foreground mt-2 truncate">
                  {file.file.name}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </Card>
  );
};