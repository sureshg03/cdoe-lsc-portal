import { useState } from 'react';
import { Search, Calendar, Users, Download, Eye, Edit } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';

export const AttendanceModule = () => {
  const [selectedMode, setSelectedMode] = useState('');
  const [selectedProgram, setSelectedProgram] = useState('');
  const [searchTerm, setSearchTerm] = useState('');

  const mockAttendanceData = [
    {
      id: 1,
      applicationNo: 'APP2024001',
      name: 'Rajesh Kumar',
      program: 'MBA',
      community: 'OBC',
      payment: 'Paid',
      attendance: '85%',
      status: 'Active'
    },
    {
      id: 2,
      applicationNo: 'APP2024002',
      name: 'Priya Sharma',
      program: 'MCA',
      community: 'General',
      payment: 'Paid',
      attendance: '92%',
      status: 'Active'
    },
    {
      id: 3,
      applicationNo: 'APP2024003',
      name: 'Amit Singh',
      program: 'M.Com',
      community: 'SC',
      payment: 'Pending',
      attendance: '78%',
      status: 'Inactive'
    }
  ];

  const getAttendanceColor = (attendance: string) => {
    const percent = parseInt(attendance);
    if (percent >= 90) return 'text-primary';
    if (percent >= 75) return 'text-education-orange';
    return 'text-destructive';
  };

  const getStatusColor = (status: string) => {
    return status === 'Active' 
      ? 'bg-primary text-primary-foreground' 
      : 'bg-muted text-muted-foreground';
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold bg-gradient-primary bg-clip-text text-transparent">
            Attendance Management
          </h1>
          <p className="text-muted-foreground mt-2">Monitor and manage student attendance records</p>
        </div>
        <div className="flex space-x-3">
          <Button variant="outline" className="shadow-soft">
            <Calendar className="w-4 h-4 mr-2" />
            Mark Attendance
          </Button>
          <Button className="bg-gradient-primary hover:opacity-90 shadow-medium">
            <Download className="w-4 h-4 mr-2" />
            Export Report
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card className="border-0 shadow-medium bg-gradient-to-br from-primary/5 to-primary/10">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-muted-foreground flex items-center">
              <Users className="w-4 h-4 mr-2" />
              Total Students
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-primary">156</div>
            <p className="text-xs text-muted-foreground mt-1">Enrolled students</p>
          </CardContent>
        </Card>

        <Card className="border-0 shadow-medium bg-gradient-to-br from-education-blue/5 to-education-blue/10">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-muted-foreground">Present Today</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-education-blue">142</div>
            <p className="text-xs text-muted-foreground mt-1">91% attendance</p>
          </CardContent>
        </Card>

        <Card className="border-0 shadow-medium bg-gradient-to-br from-education-orange/5 to-education-orange/10">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-muted-foreground">Absent Today</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-education-orange">14</div>
            <p className="text-xs text-muted-foreground mt-1">9% absent</p>
          </CardContent>
        </Card>

        <Card className="border-0 shadow-medium bg-gradient-to-br from-education-purple/5 to-education-purple/10">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-muted-foreground">Avg Attendance</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-education-purple">87%</div>
            <p className="text-xs text-muted-foreground mt-1">This month</p>
          </CardContent>
        </Card>
      </div>

      {/* Filter Card */}
      <Card className="border-0 shadow-soft">
        <CardHeader>
          <CardTitle className="text-lg font-semibold flex items-center">
            <Search className="w-5 h-5 mr-2 text-primary" />
            Filter & Search
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="space-y-2">
              <label className="text-sm font-medium text-foreground">Mode of Study</label>
              <Select value={selectedMode} onValueChange={setSelectedMode}>
                <SelectTrigger className="bg-input border-border">
                  <SelectValue placeholder="OPEN DISTANCE LEARNING" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="odl">Open Distance Learning</SelectItem>
                  <SelectItem value="regular">Regular</SelectItem>
                  <SelectItem value="online">Online</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-foreground">Programme Applied</label>
              <Select value={selectedProgram} onValueChange={setSelectedProgram}>
                <SelectTrigger className="bg-input border-border">
                  <SelectValue placeholder="Select Programme" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="mba">MBA</SelectItem>
                  <SelectItem value="mca">MCA</SelectItem>
                  <SelectItem value="mcom">M.Com</SelectItem>
                  <SelectItem value="ma">MA</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-foreground">Search</label>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <Input
                  placeholder="Search students..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 bg-input border-border"
                />
              </div>
            </div>
          </div>

          <div className="flex justify-end mt-4">
            <Button className="bg-gradient-primary hover:opacity-90 shadow-soft">
              <Search className="w-4 h-4 mr-2" />
              Search
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Attendance Table */}
      <Card className="border-0 shadow-soft">
        <CardHeader>
          <CardTitle className="text-lg font-semibold">Student Attendance Records</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="rounded-lg border border-border overflow-hidden">
            <Table>
              <TableHeader>
                <TableRow className="bg-muted/50">
                  <TableHead className="font-semibold">S.No</TableHead>
                  <TableHead className="font-semibold">Application No</TableHead>
                  <TableHead className="font-semibold">Name</TableHead>
                  <TableHead className="font-semibold">Programme</TableHead>
                  <TableHead className="font-semibold">Community</TableHead>
                  <TableHead className="font-semibold">Payment</TableHead>
                  <TableHead className="font-semibold">Attendance</TableHead>
                  <TableHead className="font-semibold">Status</TableHead>
                  <TableHead className="font-semibold">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {mockAttendanceData.map((student, index) => (
                  <TableRow key={student.id} className="hover:bg-muted/30 transition-colors">
                    <TableCell className="font-medium">{index + 1}</TableCell>
                    <TableCell className="font-mono text-sm">{student.applicationNo}</TableCell>
                    <TableCell className="font-medium">{student.name}</TableCell>
                    <TableCell>{student.program}</TableCell>
                    <TableCell>{student.community}</TableCell>
                    <TableCell>
                      <Badge className={student.payment === 'Paid' ? 'bg-primary text-primary-foreground' : 'bg-education-orange text-white'}>
                        {student.payment}
                      </Badge>
                    </TableCell>
                    <TableCell className={`font-semibold ${getAttendanceColor(student.attendance)}`}>
                      {student.attendance}
                    </TableCell>
                    <TableCell>
                      <Badge className={getStatusColor(student.status)}>
                        {student.status}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <div className="flex space-x-2">
                        <Button size="sm" variant="ghost" className="h-8 w-8 p-0 hover:bg-primary/10">
                          <Eye className="w-4 h-4 text-primary" />
                        </Button>
                        <Button size="sm" variant="ghost" className="h-8 w-8 p-0 hover:bg-education-blue/10">
                          <Edit className="w-4 h-4 text-education-blue" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>

          <div className="flex items-center justify-between mt-4">
            <p className="text-sm text-muted-foreground">
              Showing 0 to 0 of 0 entries
            </p>
            <div className="flex space-x-2">
              <Button variant="outline" size="sm" disabled>
                Previous
              </Button>
              <Button variant="outline" size="sm" disabled>
                Next
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};