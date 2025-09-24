import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Sparkles, Clock, Music, Zap } from 'lucide-react';

interface PromptInputProps {
  onGenerate: (prompt: string, style: string) => void;
  isProcessing: boolean;
}

const quickStyles = [
  { 
    label: 'Cinematic Travel',
    icon: Sparkles,
    prompt: 'Create a cinematic 2-minute highlight reel with smooth transitions and epic travel moments',
    gradient: 'bg-gradient-primary'
  },
  { 
    label: 'Instagram Reel',
    icon: Zap,
    prompt: 'Make a fun 60-second Instagram reel with upbeat energy and trendy cuts',
    gradient: 'bg-gradient-secondary'
  },
  { 
    label: 'Memory Lane',
    icon: Clock,
    prompt: 'Create a nostalgic storytelling video focusing on emotional moments and connections',
    gradient: 'bg-gradient-accent'
  },
  { 
    label: 'Music Video',
    icon: Music,
    prompt: 'Generate a rhythmic video synchronized with background music and dynamic cuts',
    gradient: 'bg-gradient-primary'
  }
];

export const PromptInput: React.FC<PromptInputProps> = ({ onGenerate, isProcessing }) => {
  const [prompt, setPrompt] = useState('');
  const [selectedStyle, setSelectedStyle] = useState('');

  const handleQuickStyle = (style: typeof quickStyles[0]) => {
    setPrompt(style.prompt);
    setSelectedStyle(style.label);
  };

  const handleGenerate = () => {
    if (prompt.trim()) {
      onGenerate(prompt, selectedStyle);
    }
  };

  return (
    <Card className="p-6 bg-card/50 backdrop-blur-sm border-border/50">
      <div className="space-y-6">
        <div>
          <h3 className="text-xl font-semibold text-foreground mb-2">
            Tell your story
          </h3>
          <p className="text-muted-foreground">
            Describe the style and mood you want for your video story
          </p>
        </div>

        <div className="space-y-4">
          <div>
            <label className="text-sm font-medium text-foreground mb-3 block">
              Quick Styles
            </label>
            <div className="grid grid-cols-2 gap-3">
              {quickStyles.map((style) => (
                <button
                  key={style.label}
                  onClick={() => handleQuickStyle(style)}
                  className={`
                    p-4 rounded-lg border border-border/50 transition-all duration-300 text-left
                    hover:border-primary/50 hover:shadow-glow group
                    ${selectedStyle === style.label ? 'border-primary bg-primary/10' : 'bg-card/30'}
                  `}
                >
                  <div className="flex items-start space-x-3">
                    <div className={`p-2 rounded-md ${style.gradient}`}>
                      <style.icon className="w-4 h-4 text-white" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="font-medium text-foreground group-hover:text-primary transition-colors">
                        {style.label}
                      </div>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>

          <div className="space-y-3">
            <label htmlFor="custom-prompt" className="text-sm font-medium text-foreground">
              Custom Prompt
            </label>
            <Textarea
              id="custom-prompt"
              placeholder="e.g., Create a 2-minute cinematic highlight of my Paris trip with romantic sunset moments and cafe scenes..."
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              className="min-h-[120px] bg-input/50 border-border/50 focus:border-primary resize-none"
            />
          </div>
        </div>

        <Button 
          onClick={handleGenerate}
          disabled={!prompt.trim() || isProcessing}
          variant="gradient"
          className="w-full hover:scale-105 transition-transform duration-300 disabled:hover:scale-100"
          size="lg"
        >
          {isProcessing ? (
            <div className="flex items-center space-x-2">
              <div className="w-4 h-4 border-2 border-primary-foreground/30 border-t-primary-foreground rounded-full animate-spin"></div>
              <span>Creating your story...</span>
            </div>
          ) : (
            <div className="flex items-center space-x-2">
              <Sparkles className="w-5 h-5" />
              <span>Generate Video Story</span>
            </div>
          )}
        </Button>
      </div>
    </Card>
  );
};