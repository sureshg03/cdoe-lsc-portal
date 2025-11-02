import { useState } from 'react';
import { 
  LayoutDashboard, 
  Settings, 
  Users, 
  UserPlus, 
  FileText, 
  BookOpen, 
  Lock, 
  LogOut,
  Menu,
  X,
  ChevronDown,
  User,
  Calendar,
  GraduationCap
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { StudentAdmissionDetails } from './modules/StudentAdmissionDetails';
import { CounsellorInformation } from './modules/CounsellorInformation';
import { AttendanceModule } from './modules/AttendanceModule';
import { AssignmentMarks } from './modules/AssignmentMarks';
import { ReportsModule } from './modules/ReportsModule';
import { ChangePassword } from './modules/ChangePassword';

interface DashboardProps {
  lscNumber: string;
  onLogout: () => void;
}

type ActivePage = 'dashboard' | 'settings' | 'admissions' | 'applications' | 'reports' | 'materials' | 'counselor' | 'attendance' | 'assignments' | 'password';

export const Dashboard = ({ lscNumber, onLogout }: DashboardProps) => {
  const [activePage, setActivePage] = useState<ActivePage>('dashboard');
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard, color: 'text-primary' },
    { id: 'settings', label: 'Settings', icon: Settings, color: 'text-education-blue' },
    { id: 'admissions', label: 'Student Admission Details', icon: Users, color: 'text-education-purple' },
    { id: 'applications', label: 'New Student Application', icon: UserPlus, color: 'text-education-orange' },
    { id: 'reports', label: 'Reports', icon: FileText, color: 'text-primary' },
    { id: 'materials', label: 'Materials', icon: BookOpen, color: 'text-education-blue' },
    { id: 'counselor', label: 'Counselor Information', icon: User, color: 'text-education-purple' },
    { id: 'attendance', label: 'Attendance', icon: Calendar, color: 'text-education-orange' },
    { id: 'assignments', label: 'Assignment Marks', icon: FileText, color: 'text-primary' },
    { id: 'password', label: 'Change Password', icon: Lock, color: 'text-education-blue' },
  ];

  const renderContent = () => {
    switch (activePage) {
      case 'dashboard':
        return (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold bg-gradient-primary bg-clip-text text-transparent">Dashboard</h1>
                <p className="text-muted-foreground mt-1">Welcome to your Learning Support Centre portal</p>
              </div>
              <Badge variant="outline" className="bg-gradient-primary text-white border-0 px-4 py-2">
                LSC: {lscNumber}
              </Badge>
            </div>

            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card className="border-0 shadow-medium bg-gradient-to-br from-primary/5 to-primary/10 hover:shadow-strong transition-all duration-300 hover:scale-[1.02]">
                <CardHeader className="pb-3">
                  <CardTitle className="text-sm font-medium text-muted-foreground">Total Applications</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold text-primary">156</div>
                  <p className="text-xs text-muted-foreground mt-1">+12% from last month</p>
                </CardContent>
              </Card>

              <Card className="border-0 shadow-medium bg-gradient-to-br from-education-blue/5 to-education-blue/10 hover:shadow-strong transition-all duration-300 hover:scale-[1.02]">
                <CardHeader className="pb-3">
                  <CardTitle className="text-sm font-medium text-muted-foreground">Enrolled Students</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold text-education-blue">89</div>
                  <p className="text-xs text-muted-foreground mt-1">+5% from last month</p>
                </CardContent>
              </Card>

              <Card className="border-0 shadow-medium bg-gradient-to-br from-education-orange/5 to-education-orange/10 hover:shadow-strong transition-all duration-300 hover:scale-[1.02]">
                <CardHeader className="pb-3">
                  <CardTitle className="text-sm font-medium text-muted-foreground">Pending Reviews</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold text-education-orange">23</div>
                  <p className="text-xs text-muted-foreground mt-1">Requires attention</p>
                </CardContent>
              </Card>

              <Card className="border-0 shadow-medium bg-gradient-to-br from-education-purple/5 to-education-purple/10 hover:shadow-strong transition-all duration-300 hover:scale-[1.02]">
                <CardHeader className="pb-3">
                  <CardTitle className="text-sm font-medium text-muted-foreground">Active Programs</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold text-education-purple">12</div>
                  <p className="text-xs text-muted-foreground mt-1">Available this semester</p>
                </CardContent>
              </Card>
            </div>

            {/* Recent Activity */}
            <Card className="border-0 shadow-medium">
              <CardHeader>
                <CardTitle className="text-xl font-semibold">Recent Activity</CardTitle>
                <CardDescription>Latest updates and applications</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center space-x-4 p-4 bg-gradient-to-r from-primary/10 to-transparent rounded-lg border border-primary/20">
                    <div className="w-3 h-3 bg-primary rounded-full animate-pulse"></div>
                    <div className="flex-1">
                      <p className="text-sm font-medium">New application submitted</p>
                      <p className="text-xs text-muted-foreground">Student ID: ST2024001 - 2 hours ago</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-4 p-4 bg-gradient-to-r from-education-blue/10 to-transparent rounded-lg border border-education-blue/20">
                    <div className="w-3 h-3 bg-education-blue rounded-full"></div>
                    <div className="flex-1">
                      <p className="text-sm font-medium">Assignment marks updated</p>
                      <p className="text-xs text-muted-foreground">Course: CS101 - 4 hours ago</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-4 p-4 bg-gradient-to-r from-education-orange/10 to-transparent rounded-lg border border-education-orange/20">
                    <div className="w-3 h-3 bg-education-orange rounded-full"></div>
                    <div className="flex-1">
                      <p className="text-sm font-medium">New counselor registered</p>
                      <p className="text-xs text-muted-foreground">Dr. Rajesh Kumar - 6 hours ago</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        );
      
      case 'admissions':
        return <StudentAdmissionDetails />;
      
      case 'counselor':
        return <CounsellorInformation />;
      
      case 'attendance':
        return <AttendanceModule />;
      
      case 'assignments':
        return <AssignmentMarks />;
      
      case 'reports':
        return <ReportsModule />;
      
      case 'password':
        return <ChangePassword />;
      
      default:
        return (
          <div className="flex items-center justify-center h-96">
            <Card className="border-0 shadow-medium max-w-md text-center">
              <CardHeader>
                <CardTitle className="text-xl">Coming Soon</CardTitle>
                <CardDescription>
                  The {menuItems.find(item => item.id === activePage)?.label} section is under development
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  This feature will be available in the next update.
                </p>
              </CardContent>
            </Card>
          </div>
        );
    }
  };

  return (
    <div className="flex h-screen bg-gradient-background">
      {/* Sidebar */}
      <div className={`${sidebarOpen ? 'w-64' : 'w-16'} transition-all duration-300 bg-card border-r border-border shadow-medium`}>
        {/* Header */}
        <div className="p-4 border-b border-border">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 flex-shrink-0 bg-gradient-primary rounded-full flex items-center justify-center">
              <GraduationCap className="w-4 h-4 text-white" />
            </div>
            {sidebarOpen && (
              <div className="min-w-0">
                <h2 className="font-semibold text-sm text-foreground truncate">Periyar University</h2>
                <p className="text-xs text-muted-foreground truncate">LSC Portal</p>
              </div>
            )}
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = activePage === item.id;
            
            return (
              <button
                key={item.id}
                onClick={() => setActivePage(item.id as ActivePage)}
                className={`w-full flex items-center space-x-3 p-3 rounded-lg text-left transition-all duration-200 ${
                  isActive 
                    ? 'bg-gradient-primary text-white shadow-soft' 
                    : 'text-foreground hover:bg-muted/50 hover:scale-[1.02]'
                }`}
              >
                <Icon className={`w-5 h-5 flex-shrink-0 ${isActive ? 'text-white' : item.color}`} />
                {sidebarOpen && (
                  <span className="truncate text-sm font-medium">{item.label}</span>
                )}
              </button>
            );
          })}
        </nav>

        {/* Logout */}
        <div className="p-4 border-t border-border">
          <button
            onClick={onLogout}
            className={`w-full flex items-center space-x-3 p-3 rounded-lg text-left transition-all duration-200 text-destructive hover:bg-destructive/10 hover:scale-[1.02]`}
          >
            <LogOut className="w-5 h-5 flex-shrink-0" />
            {sidebarOpen && <span className="truncate text-sm font-medium">Logout</span>}
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Bar */}
        <header className="bg-card border-b border-border shadow-soft px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="text-muted-foreground hover:text-foreground"
              >
                <Menu className="w-5 h-5" />
              </Button>
              <div>
                <h1 className="text-sm font-medium text-foreground">
                  LSC Name: Vidhyaa Arts & Science College
                </h1>
                <p className="text-xs text-muted-foreground">LSC No: {lscNumber}</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <Button variant="ghost" size="sm" className="bg-primary/10 text-primary">
                Create DEB ID
              </Button>
              <Button variant="ghost" size="sm" className="bg-destructive/10 text-destructive">
                Create ABC ID  
              </Button>
            </div>
          </div>
        </header>

        {/* Content */}
        <main className="flex-1 overflow-y-auto p-6">
          {renderContent()}
        </main>
      </div>
    </div>
  );
};