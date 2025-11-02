import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { useToast } from '@/hooks/use-toast';
import { Plus, Edit, Trash2, Building2, Phone, Mail, MapPin, Key, Search, X, Download, Upload, Filter, RefreshCw, Eye, Settings, Users, Calendar, TrendingUp, Sparkles } from 'lucide-react';
import api from '@/lib/api';

interface LSCUser {
  id: number;
  lsc_number: string;
  lsc_name: string;
  email: string;
  mobile: string;
  address: string;
  is_active: boolean;
  is_staff: boolean;
  date_joined: string;
}

export const LSCManagement = () => {
  const { toast } = useToast();
  const [lscCenters, setLscCenters] = useState<LSCUser[]>([]);
  const [filteredCenters, setFilteredCenters] = useState<LSCUser[]>([]);
  const [loading, setLoading] = useState(true);
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [editingLsc, setEditingLsc] = useState<LSCUser | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [formData, setFormData] = useState({
    lsc_number: '',
    lsc_name: '',
    email: '',
    mobile: '',
    address: '',
    password: ''
  });

  useEffect(() => {
    fetchLscCenters();
  }, []);

  useEffect(() => {
    if (searchTerm.trim() === '') {
      setFilteredCenters(lscCenters);
    } else {
      const filtered = lscCenters.filter(lsc =>
        lsc.lsc_number.toLowerCase().includes(searchTerm.toLowerCase()) ||
        lsc.lsc_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        lsc.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (lsc.mobile && lsc.mobile.includes(searchTerm))
      );
      setFilteredCenters(filtered);
    }
  }, [lscCenters, searchTerm]);

  const fetchLscCenters = async () => {
    try {
      setLoading(true);
      const response = await api.get('/auth/lsc-centers/');
      setLscCenters(response.data.results || []);
    } catch (error) {
      console.error('Error fetching LSC centers:', error);
      toast({
        title: "❌ Error",
        description: "Failed to load LSC centers",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const resetForm = () => {
    setFormData({
      lsc_number: '',
      lsc_name: '',
      email: '',
      mobile: '',
      address: '',
      password: ''
    });
  };

  const handleCreate = async () => {
    const existingLsc = lscCenters.find(lsc => lsc.lsc_number.toLowerCase() === formData.lsc_number.toLowerCase());
    if (existingLsc) {
      toast({
        title: "❌ Duplicate LSC Code",
        description: `LSC Center with code '${formData.lsc_number}' already exists.`,
        variant: "destructive",
      });
      return;
    }

    const existingEmail = lscCenters.find(lsc => lsc.email.toLowerCase() === formData.email.toLowerCase());
    if (existingEmail) {
      toast({
        title: "❌ Duplicate Email",
        description: `LSC Center with email '${formData.email}' already exists.`,
        variant: "destructive",
      });
      return;
    }

    try {
      await api.post('/auth/lsc-centers/', formData);
      toast({
        title: "✅ Success",
        description: `LSC Center ${formData.lsc_name} created successfully`,
      });
      setIsCreateDialogOpen(false);
      resetForm();
      fetchLscCenters();
    } catch (error: any) {
      console.error('Error creating LSC center:', error);
      const errorMessage = error.response?.data?.detail || error.response?.data?.errors || 'Failed to create LSC center';
      toast({
        title: "❌ Error",
        description: errorMessage,
        variant: "destructive",
      });
    }
  };

  const handleEdit = (lsc: LSCUser) => {
    setEditingLsc(lsc);
    setFormData({
      lsc_number: lsc.lsc_number,
      lsc_name: lsc.lsc_name,
      email: lsc.email,
      mobile: lsc.mobile || '',
      address: lsc.address || '',
      password: ''
    });
    setIsEditDialogOpen(true);
  };

  const handleUpdate = async () => {
    if (!editingLsc) return;

    const existingLsc = lscCenters.find(lsc =>
      lsc.lsc_number.toLowerCase() === formData.lsc_number.toLowerCase() && lsc.id !== editingLsc.id
    );
    if (existingLsc) {
      toast({
        title: "❌ Duplicate LSC Code",
        description: `LSC Center with code '${formData.lsc_number}' already exists.`,
        variant: "destructive",
      });
      return;
    }

    const existingEmail = lscCenters.find(lsc =>
      lsc.email.toLowerCase() === formData.email.toLowerCase() && lsc.id !== editingLsc.id
    );
    if (existingEmail) {
      toast({
        title: "❌ Duplicate Email",
        description: `LSC Center with email '${formData.email}' already exists.`,
        variant: "destructive",
      });
      return;
    }

    try {
      const updateData = { ...formData };
      if (!updateData.password) {
        delete updateData.password;
      }

      await api.put(`/auth/lsc-centers/${editingLsc.lsc_number}/`, updateData);
      toast({
        title: "✅ Success",
        description: `LSC Center ${formData.lsc_name} updated successfully`,
      });
      setIsEditDialogOpen(false);
      setEditingLsc(null);
      resetForm();
      fetchLscCenters();
    } catch (error: any) {
      console.error('Error updating LSC center:', error);
      const errorMessage = error.response?.data?.detail || error.response?.data?.errors || 'Failed to update LSC center';
      toast({
        title: "❌ Error",
        description: errorMessage,
        variant: "destructive",
      });
    }
  };

  const handleDelete = async (lsc: LSCUser) => {
    if (!confirm(`Are you sure you want to delete LSC Center ${lsc.lsc_name}?`)) {
      return;
    }

    try {
      await api.delete(`/auth/lsc-centers/${lsc.lsc_number}/`);
      toast({
        title: "✅ Success",
        description: `LSC Center ${lsc.lsc_name} deleted successfully`,
      });
      fetchLscCenters();
    } catch (error: any) {
      console.error('Error deleting LSC center:', error);
      toast({
        title: "❌ Error",
        description: "Failed to delete LSC center",
        variant: "destructive",
      });
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center h-96 space-y-4">
        <div className="relative">
          <div className="animate-spin rounded-full h-16 w-16 border-4 border-gray-200 border-t-cyan-600"></div>
          <Sparkles className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-8 h-8 text-cyan-600 animate-pulse" />
        </div>
        <p className="text-gray-600 font-medium">Loading LSC Centers...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6 relative min-h-screen pb-20">
      {/* Animated Background Gradient */}
      <div className="fixed inset-0 -z-10 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-96 h-96 bg-gradient-to-br from-cyan-300/20 to-blue-300/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-gradient-to-tr from-green-300/20 to-emerald-300/20 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }}></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-gradient-to-r from-purple-300/15 to-pink-300/15 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '0.5s' }}></div>
      </div>

      {/* Enhanced Header with Actions */}
      <div className="relative">
        <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/10 via-blue-500/10 to-purple-500/10 rounded-3xl blur-xl"></div>
        <Card className="relative border-0 shadow-2xl bg-white/90 backdrop-blur-xl overflow-hidden">
          <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-cyan-500 via-blue-500 to-purple-500"></div>
          <CardContent className="pt-8 pb-6">
            <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
              <div className="space-y-2">
                <div className="flex items-center gap-3">
                  <div className="relative">
                    <div className="absolute inset-0 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-2xl blur opacity-75"></div>
                    <div className="relative p-3 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-2xl shadow-lg">
                      <Building2 className="w-8 h-8 text-white" />
                    </div>
                  </div>
                  <div>
                    <h1 className="text-4xl font-bold bg-gradient-to-r from-cyan-600 via-blue-600 to-purple-600 bg-clip-text text-transparent flex items-center gap-2">
                      LSC Management
                      <Sparkles className="w-6 h-6 text-yellow-500 animate-pulse" />
                    </h1>
                    <p className="text-muted-foreground mt-1">
                      Create and manage LSC centers across the network
                    </p>
                  </div>
                </div>
                <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600 ml-14">
                  <div className="flex items-center gap-1.5 px-3 py-1.5 bg-gray-50 rounded-lg">
                    <Users className="w-4 h-4 text-gray-700" />
                    <span className="font-medium">{lscCenters.length} Total</span>
                  </div>
                  <div className="flex items-center gap-1.5 px-3 py-1.5 bg-green-50 rounded-lg">
                    <TrendingUp className="w-4 h-4 text-green-600" />
                    <span className="font-medium text-green-700">{lscCenters.filter(lsc => lsc.is_active).length} Active</span>
                  </div>
                  <div className="flex items-center gap-1.5 px-3 py-1.5 bg-blue-50 rounded-lg">
                    <Calendar className="w-4 h-4 text-blue-600" />
                    <span className="font-medium text-blue-700">{new Date().toLocaleDateString()}</span>
                  </div>
                </div>
              </div>
              
              <div className="flex flex-wrap gap-3">
                <Button 
                  variant="outline" 
                  className="border-2 border-gray-300 hover:bg-gray-50 hover:border-gray-400 shadow-lg"
                  onClick={fetchLscCenters}
                >
                  <RefreshCw className="w-4 h-4 mr-2" />
                  Refresh
                </Button>
                <Button 
                  variant="outline" 
                  className="border-2 border-purple-300 hover:bg-purple-50 hover:border-purple-400 shadow-lg"
                >
                  <Filter className="w-4 h-4 mr-2" />
                  Filters
                </Button>
                <Button 
                  variant="outline" 
                  className="border-2 border-blue-300 hover:bg-blue-50 hover:border-blue-400 shadow-lg"
                >
                  <Download className="w-4 h-4 mr-2" />
                  Export
                </Button>
                <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
                  <DialogTrigger asChild>
                    <Button className="bg-gradient-to-r from-cyan-600 via-blue-600 to-purple-600 hover:from-cyan-700 hover:via-blue-700 hover:to-purple-700 shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:scale-105">
                      <Plus className="w-4 h-4 mr-2" />
                      Add New LSC Center
                    </Button>
                  </DialogTrigger>
                  <DialogContent className="sm:max-w-[650px] max-h-[90vh] overflow-y-auto">
                    <DialogHeader className="border-b pb-4">
                      <div className="flex items-center gap-3">
                        <div className="relative">
                          <div className="absolute inset-0 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-xl blur opacity-75"></div>
                          <div className="relative p-3 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-xl shadow-lg">
                            <Building2 className="w-6 h-6 text-white" />
                          </div>
                        </div>
                        <div>
                          <DialogTitle className="text-2xl font-bold bg-gradient-to-r from-cyan-600 to-blue-600 bg-clip-text text-transparent">
                            Create New LSC Center
                          </DialogTitle>
                          <DialogDescription className="text-sm">
                            Add a new LSC center to the system with all required details.
                          </DialogDescription>
                        </div>
                      </div>
                    </DialogHeader>
                    <div className="grid gap-6 py-6">
                      {/* LSC Code and Name Row */}
                      <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <Label htmlFor="lsc_number" className="flex items-center gap-2 font-semibold text-gray-700">
                            <Key className="w-4 h-4 text-cyan-600" />
                            LSC Code *
                          </Label>
                          <Input
                            id="lsc_number"
                            placeholder="e.g., LC2101"
                            value={formData.lsc_number}
                            onChange={(e) => handleInputChange('lsc_number', e.target.value)}
                            className="border-2 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-200"
                          />
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor="lsc_name" className="flex items-center gap-2 font-semibold text-gray-700">
                            <Building2 className="w-4 h-4 text-blue-600" />
                            LSC Name *
                          </Label>
                          <Input
                            id="lsc_name"
                            placeholder="e.g., CDEO LSC Center"
                            value={formData.lsc_name}
                            onChange={(e) => handleInputChange('lsc_name', e.target.value)}
                            className="border-2 focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
                          />
                        </div>
                      </div>

                      {/* Email and Mobile Row */}
                      <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <Label htmlFor="email" className="flex items-center gap-2 font-semibold text-gray-700">
                            <Mail className="w-4 h-4 text-purple-600" />
                            Email ID *
                          </Label>
                          <Input
                            id="email"
                            type="email"
                            placeholder="lsc@example.com"
                            value={formData.email}
                            onChange={(e) => handleInputChange('email', e.target.value)}
                            className="border-2 focus:border-purple-500 focus:ring-2 focus:ring-purple-200"
                          />
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor="mobile" className="flex items-center gap-2 font-semibold text-gray-700">
                            <Phone className="w-4 h-4 text-green-600" />
                            Mobile Number
                          </Label>
                          <Input
                            id="mobile"
                            placeholder="+91 9876543210"
                            value={formData.mobile}
                            onChange={(e) => handleInputChange('mobile', e.target.value)}
                            className="border-2 focus:border-green-500 focus:ring-2 focus:ring-green-200"
                          />
                        </div>
                      </div>

                      {/* Address Field */}
                      <div className="space-y-2">
                        <Label htmlFor="address" className="flex items-center gap-2 font-semibold text-gray-700">
                          <MapPin className="w-4 h-4 text-orange-600" />
                          Address
                        </Label>
                        <Textarea
                          id="address"
                          placeholder="Full address of the LSC center"
                          value={formData.address}
                          onChange={(e) => handleInputChange('address', e.target.value)}
                          rows={3}
                          className="border-2 focus:border-orange-500 focus:ring-2 focus:ring-orange-200 resize-none"
                        />
                      </div>

                      {/* Password Field */}
                      <div className="space-y-2">
                        <Label htmlFor="password" className="flex items-center gap-2 font-semibold text-gray-700">
                          <Key className="w-4 h-4 text-red-600" />
                          LSC Password *
                        </Label>
                        <Input
                          id="password"
                          type="password"
                          placeholder="Enter secure password (min 8 characters)"
                          value={formData.password}
                          onChange={(e) => handleInputChange('password', e.target.value)}
                          className="border-2 focus:border-red-500 focus:ring-2 focus:ring-red-200"
                        />
                        <div className="flex items-start gap-2 text-xs text-gray-600 bg-gray-50 p-3 rounded-lg">
                          <Sparkles className="w-4 h-4 text-yellow-500 flex-shrink-0 mt-0.5" />
                          <span>Password must include uppercase letters, numbers, and be at least 8 characters long</span>
                        </div>
                      </div>
                    </div>
                    <DialogFooter className="border-t pt-4 bg-gradient-to-r from-gray-50 to-gray-100">
                      <Button 
                        variant="outline" 
                        onClick={() => { setIsCreateDialogOpen(false); resetForm(); }}
                        className="border-2 hover:bg-gray-100"
                      >
                        <X className="w-4 h-4 mr-2" />
                        Cancel
                      </Button>
                      <Button 
                        onClick={handleCreate} 
                        className="bg-gradient-to-r from-cyan-600 via-blue-600 to-purple-600 hover:from-cyan-700 hover:via-blue-700 hover:to-purple-700 shadow-lg hover:shadow-xl"
                      >
                        <Plus className="w-4 h-4 mr-2" />
                        Create LSC Center
                      </Button>
                    </DialogFooter>
                  </DialogContent>
                </Dialog>
                
                <Button 
                  onClick={() => setIsCreateDialogOpen(true)}
                  className="bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:scale-105"
                >
                  <Sparkles className="w-4 h-4 mr-2" />
                  MORE LSC CENTERS
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Enhanced Search Bar */}
      <Card className="border-0 shadow-xl bg-gradient-to-r from-white via-cyan-50/30 to-blue-50/30 overflow-hidden">
        <div className="absolute top-0 left-0 right-0 h-0.5 bg-gradient-to-r from-cyan-400 via-blue-400 to-purple-400"></div>
        <CardContent className="pt-6 pb-6">
          <div className="relative group">
            <div className="absolute inset-0 bg-gradient-to-r from-cyan-400 to-blue-500 rounded-xl opacity-0 group-hover:opacity-5 transition-opacity"></div>
            <div className="absolute left-4 top-1/2 transform -translate-y-1/2 p-2 bg-cyan-100 rounded-lg z-10">
              <Search className="text-cyan-600 w-5 h-5" />
            </div>
            <Input
              placeholder="🔍 Search LSC centers by code, name, email, or mobile number..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-16 pr-14 h-14 text-base border-2 border-gray-300 focus:border-cyan-500 rounded-xl shadow-lg hover:shadow-xl transition-all font-medium"
            />
            {searchTerm && (
              <button
                onClick={() => setSearchTerm('')}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 p-2 rounded-lg bg-red-100 hover:bg-red-200 text-red-600 transition-all z-10 group"
                title="Clear search"
              >
                <X className="w-5 h-5" />
              </button>
            )}
          </div>
          {searchTerm && (
            <div className={`mt-4 flex items-center justify-between rounded-xl p-4 border-2 ${
              filteredCenters.length === 0 
                ? 'bg-gradient-to-r from-red-50 to-orange-50 border-red-300' 
                : 'bg-gradient-to-r from-green-50 to-emerald-50 border-green-300'
            }`}>
              <p className="text-sm font-semibold flex items-center gap-2">
                {filteredCenters.length === 0 ? (
                  <>
                    <X className="w-5 h-5 text-red-600" />
                    <span className="text-red-700">No LSC centers found matching "{searchTerm}"</span>
                  </>
                ) : (
                  <>
                    <Search className="w-5 h-5 text-green-600" />
                    <span className="text-green-700">
                      Found {filteredCenters.length} LSC center{filteredCenters.length === 1 ? '' : 's'} matching "{searchTerm}"
                    </span>
                  </>
                )}
              </p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="border-0 shadow-xl bg-gradient-to-br from-cyan-50 via-cyan-100 to-cyan-50 hover:shadow-2xl transition-all duration-300 hover:scale-105 relative overflow-hidden group">
          <div className="absolute top-0 right-0 w-32 h-32 bg-cyan-300/20 rounded-full blur-2xl group-hover:scale-150 transition-transform"></div>
          <CardHeader className="pb-3 relative z-10">
            <CardTitle className="text-sm font-semibold text-gray-600 flex items-center gap-2">
              <Users className="w-4 h-4" />
              {searchTerm ? 'Matching Centers' : 'Total LSC Centers'}
            </CardTitle>
          </CardHeader>
          <CardContent className="relative z-10">
            <div className="text-4xl font-bold text-cyan-700">{filteredCenters.length}</div>
            <p className="text-xs text-gray-500 mt-2">
              {searchTerm ? `of ${lscCenters.length} total centers` : 'Registered centers'}
            </p>
          </CardContent>
        </Card>

        <Card className="border-0 shadow-xl bg-gradient-to-br from-blue-50 via-blue-100 to-blue-50 hover:shadow-2xl transition-all duration-300 hover:scale-105 relative overflow-hidden group">
          <div className="absolute top-0 right-0 w-32 h-32 bg-blue-300/20 rounded-full blur-2xl group-hover:scale-150 transition-transform"></div>
          <CardHeader className="pb-3 relative z-10">
            <CardTitle className="text-sm font-semibold text-gray-600 flex items-center gap-2">
              <TrendingUp className="w-4 h-4" />
              Active Centers
            </CardTitle>
          </CardHeader>
          <CardContent className="relative z-10">
            <div className="text-4xl font-bold text-blue-700">
              {filteredCenters.filter(lsc => lsc.is_active).length}
            </div>
            <p className="text-xs text-gray-500 mt-2">Currently operational</p>
          </CardContent>
        </Card>

        <Card className="border-0 shadow-xl bg-gradient-to-br from-green-50 via-green-100 to-green-50 hover:shadow-2xl transition-all duration-300 hover:scale-105 relative overflow-hidden group">
          <div className="absolute top-0 right-0 w-32 h-32 bg-green-300/20 rounded-full blur-2xl group-hover:scale-150 transition-transform"></div>
          <CardHeader className="pb-3 relative z-10">
            <CardTitle className="text-sm font-semibold text-gray-600 flex items-center gap-2">
              <Settings className="w-4 h-4" />
              Staff Members
            </CardTitle>
          </CardHeader>
          <CardContent className="relative z-10">
            <div className="text-4xl font-bold text-green-700">
              {filteredCenters.filter(lsc => lsc.is_staff).length}
            </div>
            <p className="text-xs text-gray-500 mt-2">With staff privileges</p>
          </CardContent>
        </Card>

        <Card className="border-0 shadow-xl bg-gradient-to-br from-purple-50 via-purple-100 to-purple-50 hover:shadow-2xl transition-all duration-300 hover:scale-105 relative overflow-hidden group">
          <div className="absolute top-0 right-0 w-32 h-32 bg-purple-300/20 rounded-full blur-2xl group-hover:scale-150 transition-transform"></div>
          <CardHeader className="pb-3 relative z-10">
            <CardTitle className="text-sm font-semibold text-gray-600 flex items-center gap-2">
              <Calendar className="w-4 h-4" />
              New This Month
            </CardTitle>
          </CardHeader>
          <CardContent className="relative z-10">
            <div className="text-4xl font-bold text-purple-700">
              {filteredCenters.filter(lsc => {
                const joinedDate = new Date(lsc.date_joined);
                const now = new Date();
                return joinedDate.getMonth() === now.getMonth() && joinedDate.getFullYear() === now.getFullYear();
              }).length}
            </div>
            <p className="text-xs text-gray-500 mt-2">Recently added</p>
          </CardContent>
        </Card>
      </div>

      {/* LSC Centers Table */}
      <Card className="border-0 shadow-2xl overflow-hidden">
        <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-cyan-500 via-blue-500 via-purple-500 to-pink-500"></div>
        <CardHeader className="flex flex-row items-center justify-between bg-gradient-to-r from-gray-50 to-gray-100 border-b">
          <div>
            <CardTitle className="text-2xl font-bold bg-gradient-to-r from-cyan-600 to-blue-600 bg-clip-text text-transparent flex items-center gap-2">
              <Building2 className="w-6 h-6 text-cyan-600" />
              LSC Centers Directory
            </CardTitle>
            <CardDescription className="mt-1">
              Comprehensive list of all LSC centers in the system
            </CardDescription>
          </div>
          {filteredCenters.length > 0 && (
            <Button 
              onClick={() => setIsCreateDialogOpen(true)}
              className="bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 shadow-lg hover:shadow-xl"
            >
              <Plus className="w-4 h-4 mr-2" />
              MORE LSC CENTERS
            </Button>
          )}
        </CardHeader>
        <CardContent className="p-0">
          {filteredCenters.length === 0 ? (
            <div className="text-center py-16 px-4">
              <div className="relative inline-block mb-6">
                <div className="absolute inset-0 bg-gradient-to-br from-cyan-200 to-blue-200 rounded-3xl blur-xl opacity-50"></div>
                <div className="relative bg-gradient-to-br from-cyan-100 to-blue-100 p-8 rounded-3xl">
                  <Building2 className="w-20 h-20 text-cyan-600 mx-auto" />
                </div>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">
                {searchTerm ? 'No LSC Centers Found' : 'No LSC Centers Yet'}
              </h3>
              <p className="text-gray-500 mb-6 max-w-md mx-auto">
                {searchTerm
                  ? `No centers match your search for "${searchTerm}". Try adjusting your search terms or clear the filter.`
                  : 'Get started by creating your first LSC center to begin managing your educational network'
                }
              </p>
              {!searchTerm && (
                <div className="flex gap-3 justify-center flex-wrap">
                  <Button 
                    onClick={() => setIsCreateDialogOpen(true)} 
                    className="bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-700 hover:to-blue-700 shadow-lg hover:shadow-xl"
                    size="lg"
                  >
                    <Plus className="w-5 h-5 mr-2" />
                    Add First LSC Center
                  </Button>
                  <Button 
                    onClick={() => setIsCreateDialogOpen(true)} 
                    variant="outline" 
                    className="border-2 border-green-300 hover:bg-green-50 hover:border-green-400 shadow-lg"
                    size="lg"
                  >
                    <Sparkles className="w-5 h-5 mr-2" />
                    MORE LSC CENTERS
                  </Button>
                </div>
              )}
            </div>
          ) : (
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow className="bg-gradient-to-r from-gray-50 to-gray-100 hover:from-gray-100 hover:to-gray-150">
                    <TableHead className="font-bold text-gray-700">LSC Code</TableHead>
                    <TableHead className="font-bold text-gray-700">Name</TableHead>
                    <TableHead className="font-bold text-gray-700">Contact</TableHead>
                    <TableHead className="font-bold text-gray-700">Status</TableHead>
                    <TableHead className="font-bold text-gray-700">Joined</TableHead>
                    <TableHead className="text-right font-bold text-gray-700">Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredCenters.map((lsc, index) => (
                    <TableRow 
                      key={lsc.id} 
                      className={`hover:bg-gradient-to-r hover:from-cyan-50 hover:to-blue-50 transition-all ${
                        index % 2 === 0 ? 'bg-white' : 'bg-gray-50/50'
                      }`}
                    >
                      <TableCell className="font-semibold">
                        <div className="flex items-center gap-2">
                          <div className="p-2 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-lg">
                            <Building2 className="w-4 h-4 text-white" />
                          </div>
                          <span className="text-cyan-700">{lsc.lsc_number}</span>
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="font-medium text-gray-900">{lsc.lsc_name}</div>
                      </TableCell>
                      <TableCell>
                        <div className="space-y-1.5">
                          <div className="flex items-center gap-2 text-sm text-gray-600">
                            <Mail className="w-3.5 h-3.5 text-purple-500" />
                            <span className="font-medium">{lsc.email}</span>
                          </div>
                          {lsc.mobile && (
                            <div className="flex items-center gap-2 text-sm text-gray-600">
                              <Phone className="w-3.5 h-3.5 text-green-500" />
                              <span className="font-medium">{lsc.mobile}</span>
                            </div>
                          )}
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="flex flex-wrap gap-2">
                          <Badge 
                            variant={lsc.is_active ? "default" : "secondary"}
                            className={lsc.is_active 
                              ? "bg-gradient-to-r from-green-500 to-emerald-500 text-white shadow-md" 
                              : "bg-gray-300 text-gray-700"
                            }
                          >
                            {lsc.is_active ? '● Active' : '○ Inactive'}
                          </Badge>
                          {lsc.is_staff && (
                            <Badge variant="outline" className="border-blue-300 text-blue-700 bg-blue-50">
                              Staff
                            </Badge>
                          )}
                        </div>
                      </TableCell>
                      <TableCell>
                        <span className="text-sm text-gray-600 font-medium">
                          {new Date(lsc.date_joined).toLocaleDateString('en-US', { 
                            year: 'numeric', 
                            month: 'short', 
                            day: 'numeric' 
                          })}
                        </span>
                      </TableCell>
                      <TableCell className="text-right">
                        <div className="flex justify-end gap-2">
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleEdit(lsc)}
                            className="border-2 border-blue-300 hover:bg-blue-50 hover:border-blue-400 text-blue-700 shadow-md hover:shadow-lg"
                            title="Edit LSC Center"
                          >
                            <Edit className="w-4 h-4" />
                          </Button>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleDelete(lsc)}
                            className="border-2 border-red-300 hover:bg-red-50 hover:border-red-400 text-red-700 shadow-md hover:shadow-lg"
                            title="Delete LSC Center"
                          >
                            <Trash2 className="w-4 h-4" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Edit Dialog */}
      <Dialog open={isEditDialogOpen} onOpenChange={setIsEditDialogOpen}>
        <DialogContent className="sm:max-w-[650px] max-h-[90vh] overflow-y-auto">
          <DialogHeader className="border-b pb-4">
            <div className="flex items-center gap-3">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl blur opacity-75"></div>
                <div className="relative p-3 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl shadow-lg">
                  <Edit className="w-6 h-6 text-white" />
                </div>
              </div>
              <div>
                <DialogTitle className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  Edit LSC Center
                </DialogTitle>
                <DialogDescription className="text-sm">
                  Update the details of {editingLsc?.lsc_name}
                </DialogDescription>
              </div>
            </div>
          </DialogHeader>
          <div className="grid gap-6 py-6">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="edit_lsc_number" className="flex items-center gap-2 font-semibold text-gray-700">
                  <Key className="w-4 h-4 text-cyan-600" />
                  LSC Code *
                </Label>
                <Input
                  id="edit_lsc_number"
                  value={formData.lsc_number}
                  onChange={(e) => handleInputChange('lsc_number', e.target.value)}
                  className="border-2 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-200"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="edit_lsc_name" className="flex items-center gap-2 font-semibold text-gray-700">
                  <Building2 className="w-4 h-4 text-blue-600" />
                  LSC Name *
                </Label>
                <Input
                  id="edit_lsc_name"
                  value={formData.lsc_name}
                  onChange={(e) => handleInputChange('lsc_name', e.target.value)}
                  className="border-2 focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
                />
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="edit_email" className="flex items-center gap-2 font-semibold text-gray-700">
                  <Mail className="w-4 h-4 text-purple-600" />
                  Email ID *
                </Label>
                <Input
                  id="edit_email"
                  type="email"
                  value={formData.email}
                  onChange={(e) => handleInputChange('email', e.target.value)}
                  className="border-2 focus:border-purple-500 focus:ring-2 focus:ring-purple-200"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="edit_mobile" className="flex items-center gap-2 font-semibold text-gray-700">
                  <Phone className="w-4 h-4 text-green-600" />
                  Mobile Number
                </Label>
                <Input
                  id="edit_mobile"
                  value={formData.mobile}
                  onChange={(e) => handleInputChange('mobile', e.target.value)}
                  className="border-2 focus:border-green-500 focus:ring-2 focus:ring-green-200"
                />
              </div>
            </div>
            <div className="space-y-2">
              <Label htmlFor="edit_address" className="flex items-center gap-2 font-semibold text-gray-700">
                <MapPin className="w-4 h-4 text-orange-600" />
                Address
              </Label>
              <Textarea
                id="edit_address"
                value={formData.address}
                onChange={(e) => handleInputChange('address', e.target.value)}
                rows={3}
                className="border-2 focus:border-orange-500 focus:ring-2 focus:ring-orange-200 resize-none"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="edit_password" className="flex items-center gap-2 font-semibold text-gray-700">
                <Key className="w-4 h-4 text-red-600" />
                New Password (optional)
              </Label>
              <Input
                id="edit_password"
                type="password"
                placeholder="Leave empty to keep current password"
                value={formData.password}
                onChange={(e) => handleInputChange('password', e.target.value)}
                className="border-2 focus:border-red-500 focus:ring-2 focus:ring-red-200"
              />
              <div className="flex items-start gap-2 text-xs text-gray-600 bg-yellow-50 p-3 rounded-lg border border-yellow-200">
                <Sparkles className="w-4 h-4 text-yellow-600 flex-shrink-0 mt-0.5" />
                <span>Leave password field empty to keep the current password unchanged</span>
              </div>
            </div>
          </div>
          <DialogFooter className="border-t pt-4 bg-gradient-to-r from-gray-50 to-gray-100">
            <Button 
              variant="outline" 
              onClick={() => { setIsEditDialogOpen(false); setEditingLsc(null); resetForm(); }}
              className="border-2 hover:bg-gray-100"
            >
              <X className="w-4 h-4 mr-2" />
              Cancel
            </Button>
            <Button 
              onClick={handleUpdate} 
              className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 shadow-lg hover:shadow-xl"
            >
              <Edit className="w-4 h-4 mr-2" />
              Update LSC Center
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Floating Action Button */}
      <div className="fixed bottom-8 right-8 z-50 group">
        <Button
          onClick={() => setIsCreateDialogOpen(true)}
          size="lg"
          className="rounded-full w-16 h-16 bg-gradient-to-br from-green-600 via-emerald-600 to-teal-600 hover:from-green-700 hover:via-emerald-700 hover:to-teal-700 shadow-2xl hover:shadow-3xl transition-all duration-300 transform hover:scale-110 border-4 border-white relative overflow-hidden"
          title="Add More LSC Centers"
        >
          <div className="absolute inset-0 bg-white/20 rounded-full animate-ping"></div>
          <Plus className="w-8 h-8 relative z-10" />
        </Button>
        <div className="absolute bottom-full right-0 mb-4 px-4 py-2 bg-gray-900 text-white text-sm font-medium rounded-lg opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap shadow-xl">
          MORE LSC CENTERS
          <div className="absolute top-full right-8 w-0 h-0 border-l-8 border-r-8 border-t-8 border-transparent border-t-gray-900"></div>
        </div>
      </div>
    </div>
  );
};