import React, { useState } from 'react';
import { UploadZone } from '@/components/UploadZone';
import { PromptInput } from '@/components/PromptInput';
import { VideoPreview } from '@/components/VideoPreview';
import { Button } from '@/components/ui/button';
import { Sparkles, Video, Wand2 } from 'lucide-react';

interface UploadedFile {
  id: string;
  file: File;
  preview?: string;
  type: 'video' | 'image';
}

const Index = () => {
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [currentPrompt, setCurrentPrompt] = useState('');
  const [currentStyle, setCurrentStyle] = useState('');
  const [generatedVideoUrl, setGeneratedVideoUrl] = useState<string>('');

  const handleFilesUpload = async (files: UploadedFile[]) => {
    setUploadedFiles(prev => [...prev, ...files]);
  
    // Prepare form data
    const formData = new FormData();
    files.forEach(fileObj => {
      formData.append("files", fileObj.file);  // 👈 matches FastAPI param
    });
  
    try {
      const response = await fetch("http://127.0.0.1:8000/upload/", {
        method: "POST",
        body: formData,
      });
  
      const data = await response.json();
      console.log("Uploaded successfully:", data);
    } catch (error) {
      console.error("Upload failed:", error);
    }
  };  

  const handleGenerate = async (prompt: string, style: string) => {
    setCurrentPrompt(prompt);
    setCurrentStyle(style);
    setIsProcessing(true);
    setGeneratedVideoUrl('');
    
    // Simulate AI processing
    setTimeout(() => {
      setIsProcessing(false);
      // For demo purposes, we'll use a sample video URL
      setGeneratedVideoUrl('https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_2mb.mp4');
    }, 8000);
  };

  return (
    <div className="min-h-screen bg-gradient-cosmic">
      {/* Header */}
      <header className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-primary/10 backdrop-blur-sm"></div>
        <div className="relative container mx-auto px-6 py-8">
          <div className="text-center space-y-4">
            <div className="flex items-center justify-center space-x-3">
              <div className="p-3 bg-gradient-primary rounded-xl">
                <Video className="w-8 h-8 text-white" />
              </div>
              <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-primary to-primary-glow bg-clip-text text-transparent">
                Trip Story AI
              </h1>
            </div>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Transform your travel memories into cinematic stories with the power of AI
            </p>
            <div className="flex items-center justify-center space-x-6 text-sm text-muted-foreground">
              <div className="flex items-center space-x-2">
                <Sparkles className="w-4 h-4 text-primary" />
                <span>AI-Powered Editing</span>
              </div>
              <div className="flex items-center space-x-2">
                <Wand2 className="w-4 h-4 text-secondary" />
                <span>Custom Storytelling</span>
              </div>
              <div className="flex items-center space-x-2">
                <Video className="w-4 h-4 text-accent" />
                <span>Professional Quality</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-8">
        <div className="grid lg:grid-cols-2 gap-8 max-w-7xl mx-auto">
          {/* Left Column - Upload & Prompt */}
          <div className="space-y-8">
            <div className="space-y-4">
              <h2 className="text-2xl font-semibold text-foreground flex items-center">
                <span className="w-8 h-8 bg-gradient-primary rounded-full flex items-center justify-center text-primary-foreground text-sm font-bold mr-3">
                  1
                </span>
                Upload Your Content
              </h2>
              <UploadZone 
                onFilesUpload={handleFilesUpload}
                uploadedFiles={uploadedFiles}
              />
            </div>

            <div className="space-y-4">
              <h2 className="text-2xl font-semibold text-foreground flex items-center">
                <span className="w-8 h-8 bg-gradient-secondary rounded-full flex items-center justify-center text-secondary-foreground text-sm font-bold mr-3">
                  2
                </span>
                Describe Your Vision
              </h2>
              <PromptInput 
                onGenerate={handleGenerate}
                isProcessing={isProcessing}
              />
            </div>
          </div>

          {/* Right Column - Preview */}
          <div className="space-y-4">
            <h2 className="text-2xl font-semibold text-foreground flex items-center">
              <span className="w-8 h-8 bg-gradient-accent rounded-full flex items-center justify-center text-accent-foreground text-sm font-bold mr-3">
                3
              </span>
              Your Story Awaits
            </h2>
            <div className="sticky top-8">
              <VideoPreview 
                isProcessing={isProcessing}
                videoUrl={generatedVideoUrl}
                prompt={currentPrompt}
                style={currentStyle}
              />
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="relative mt-20 py-8 border-t border-border/50">
        <div className="container mx-auto px-6 text-center">
          <p className="text-muted-foreground">
            Transform your travel memories into unforgettable stories with AI
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Index;
