import React from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Download, Share2, RefreshCw, Play, Pause } from 'lucide-react';

interface VideoPreviewProps {
  isProcessing: boolean;
  videoUrl?: string;
  prompt?: string;
  style?: string;
}

export const VideoPreview: React.FC<VideoPreviewProps> = ({ 
  isProcessing, 
  videoUrl, 
  prompt,
  style 
}) => {
  const [isPlaying, setIsPlaying] = React.useState(false);

  if (isProcessing) {
    return (
      <Card className="p-8 bg-card/50 backdrop-blur-sm border-border/50">
        <div className="text-center space-y-6">
          <div className="relative mx-auto w-32 h-32">
            <div className="absolute inset-0 border-4 border-primary/20 rounded-full"></div>
            <div className="absolute inset-0 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
            <div className="absolute inset-4 bg-gradient-primary rounded-full flex items-center justify-center">
              <RefreshCw className="w-8 h-8 text-white animate-pulse" />
            </div>
          </div>
          
          <div className="space-y-2">
            <h3 className="text-2xl font-semibold text-foreground">
              Crafting your story...
            </h3>
            <p className="text-muted-foreground max-w-md mx-auto">
              AI is analyzing your content, selecting the best moments, and weaving them into an amazing video story.
            </p>
          </div>

          <div className="space-y-2">
            <div className="flex justify-center space-x-2 text-sm text-muted-foreground">
              <span>•</span>
              <span>Analyzing content</span>
              <span>•</span>
              <span>Selecting highlights</span>
              <span>•</span>
              <span>Adding magic</span>
            </div>
            <div className="w-full max-w-md mx-auto bg-muted rounded-full h-2">
              <div className="bg-gradient-primary h-2 rounded-full animate-pulse" style={{ width: '65%' }}></div>
            </div>
          </div>
        </div>
      </Card>
    );
  }

  if (videoUrl) {
    return (
      <Card className="overflow-hidden bg-card/50 backdrop-blur-sm border-border/50">
        <div className="relative aspect-video bg-muted">
          <video 
            className="w-full h-full object-cover"
            controls
            onPlay={() => setIsPlaying(true)}
            onPause={() => setIsPlaying(false)}
          >
            <source src={videoUrl} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
          
          {!isPlaying && (
            <div className="absolute inset-0 bg-black/20 flex items-center justify-center">
              <Button 
                size="lg"
                variant="gradient"
                className="hover:scale-105 transition-transform duration-300"
              >
                <Play className="w-6 h-6 mr-2" />
                Play Story
              </Button>
            </div>
          )}
        </div>

        <div className="p-6 space-y-4">
          <div className="flex items-center justify-between">
            <div className="space-y-1">
              <h3 className="text-xl font-semibold text-foreground">
                Your Video Story
              </h3>
              {style && (
                <Badge variant="outline" className="text-xs">
                  {style}
                </Badge>
              )}
            </div>
          </div>

          {prompt && (
            <p className="text-sm text-muted-foreground bg-muted/50 p-3 rounded-lg">
              {prompt}
            </p>
          )}

          <div className="flex space-x-3">
            <Button 
              variant="gradient"
              className="flex-1 hover:scale-105 transition-transform duration-300"
            >
              <Download className="w-4 h-4 mr-2" />
              Download
            </Button>
            <Button 
              variant="outline"
              className="bg-card/50 border-border/50 hover:bg-gradient-accent hover:text-accent-foreground hover:border-0"
            >
              <Share2 className="w-4 h-4 mr-2" />
              Share
            </Button>
          </div>
        </div>
      </Card>
    );
  }

  return (
    <Card className="p-8 bg-card/30 backdrop-blur-sm border-border/30 border-dashed">
      <div className="text-center space-y-4 opacity-60">
        <div className="w-16 h-16 mx-auto bg-muted/50 rounded-full flex items-center justify-center">
          <Play className="w-8 h-8 text-muted-foreground" />
        </div>
        <div>
          <h3 className="text-lg font-medium text-muted-foreground">
            Ready to create magic?
          </h3>
          <p className="text-sm text-muted-foreground/80">
            Upload your content and describe your vision to get started
          </p>
        </div>
      </div>
    </Card>
  );
};