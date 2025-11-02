import { useState } from 'react';
import { Eye, EyeOff, User, Lock, GraduationCap } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { useToast } from '@/hooks/use-toast';
import { authAPI } from '@/lib/api';

interface LoginPageProps {
  onLogin: (lscNumber: string) => void;
}

export const LoginPage = ({ onLogin }: LoginPageProps) => {
  const [lscNumber, setLscNumber] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!lscNumber || !password) {
      toast({
        title: "Error",
        description: "Please fill in all fields",
        variant: "destructive",
      });
      return;
    }

    setIsLoading(true);

    try {
      const response = await authAPI.login(lscNumber, password);
      const { access, refresh } = response.data;

      // Store tokens
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);

      onLogin(lscNumber);
      toast({
        title: "Success",
        description: "Logged in successfully",
      });
    } catch (error: any) {
      toast({
        title: "Error",
        description: error.response?.data?.detail || "Login failed",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-background flex flex-col items-center justify-center p-4">
      {/* University Header */}
      <div className="text-center mb-8 space-y-4">
        <div className="flex items-center justify-center mb-6">
          <div className="w-20 h-20 mr-4 bg-gradient-primary rounded-full flex items-center justify-center shadow-medium">
            <GraduationCap className="w-10 h-10 text-white" />
          </div>
          <div className="text-left">
            <h1 className="text-3xl font-bold text-primary mb-1">Periyar University</h1>
            <p className="text-sm text-muted-foreground">NAAC 'A++' Grade with CGPA 3.61 (Cycle - 3)</p>
            <p className="text-sm text-muted-foreground">State University - NIRF Rank 56 - State Public University Rank 25</p>
            <p className="text-sm text-muted-foreground">Salem-636011, Tamilnadu, India.</p>
          </div>
        </div>
        
        <div className="space-y-2">
          <h2 className="text-2xl font-bold bg-gradient-primary bg-clip-text text-transparent">
            CENTRE FOR DISTANCE AND ONLINE EDUCATION (CDOE)
          </h2>
          <p className="text-lg text-education-orange font-semibold">Open and Distance Learning</p>
        </div>
      </div>

      {/* Login Card */}
      <Card className="w-full max-w-md shadow-strong border-0 bg-card/80 backdrop-blur-sm">
        <CardHeader className="text-center space-y-4">
          <div className="flex items-center justify-center w-16 h-16 mx-auto bg-gradient-primary rounded-full shadow-medium">
            <GraduationCap className="w-8 h-8 text-white" />
          </div>
          <div>
            <CardTitle className="text-2xl font-bold text-destructive">
              Learning Support Centre Login
            </CardTitle>
            <CardDescription className="text-muted-foreground mt-2">
              Access your LSC dashboard to manage student applications and reports
            </CardDescription>
          </div>
        </CardHeader>

        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="lscNumber" className="text-sm font-medium text-foreground">
                LSC Number *
              </Label>
              <div className="relative">
                <User className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <Input
                  id="lscNumber"
                  type="text"
                  placeholder="LSC Number (Ex: LC2101)"
                  value={lscNumber}
                  onChange={(e) => setLscNumber(e.target.value)}
                  className="pl-10 h-12 bg-input border-border focus:ring-2 focus:ring-primary focus:border-transparent transition-all duration-200"
                  required
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="password" className="text-sm font-medium text-foreground">
                Password *
              </Label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <Input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="pl-10 pr-10 h-12 bg-input border-border focus:ring-2 focus:ring-primary focus:border-transparent transition-all duration-200"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>

            <Button 
              type="submit" 
              className="w-full h-12 bg-gradient-primary hover:opacity-90 text-primary-foreground font-semibold text-base shadow-medium transition-all duration-200 hover:shadow-strong hover:scale-[1.02] active:scale-[0.98]"
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin mr-2" />
                  Signing In...
                </>
              ) : (
                'Login'
              )}
            </Button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-sm text-muted-foreground">
              Having trouble? Contact your administrator for assistance.
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Footer */}
      <div className="mt-8 text-center text-sm text-muted-foreground">
        <p>© 2024 Periyar University. All rights reserved.</p>
      </div>
    </div>
  );
};