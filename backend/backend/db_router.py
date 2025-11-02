"""
Database Router for Multi-Database Setup
Routes models to appropriate databases:
- LSCAdmin -> online_edu database (lsc_admins table)
- LSCUser -> default database (lsc_portal_db)
- portal app models -> lsc_admindb database
"""

class LSCDatabaseRouter:
    """
    A router to control database operations for LSC models.
    - LSCAdmin -> online_edu database (lsc_admins table)
    - LSCUser -> default database (lsc_portal_db)
    - portal app (ApplicationSettings, etc) -> lsc_admindb database
    """
    
    def db_for_read(self, model, **hints):
        """
        Route read operations based on model
        """
        # Route portal app models to lsc_admindb
        if model._meta.app_label == 'portal':
            return 'lsc_admindb'
        
        # Route lsc_auth models
        if model._meta.app_label == 'lsc_auth':
            # LSCAdmin goes to online_edu
            if model.__name__ == 'LSCAdmin':
                return 'online_edu'
            # LSCUser goes to default
            return 'default'
        
        return None  # Let Django decide for other apps
    
    def db_for_write(self, model, **hints):
        """
        Route write operations based on model
        """
        # Route portal app models to lsc_admindb
        if model._meta.app_label == 'portal':
            return 'lsc_admindb'
        
        # Route lsc_auth models
        if model._meta.app_label == 'lsc_auth':
            # LSCAdmin goes to online_edu
            if model.__name__ == 'LSCAdmin':
                return 'online_edu'
            # LSCUser goes to default
            return 'default'
        
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations between objects in the same database
        """
        # Allow relations within the same app
        if obj1._meta.app_label == obj2._meta.app_label:
            return True
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Control which database migrations run on
        """
        # Route portal app migrations to lsc_admindb
        if app_label == 'portal':
            return db == 'lsc_admindb'
        
        # Route lsc_auth migrations
        if app_label == 'lsc_auth':
            if model_name == 'lscadmin':
                # Don't migrate LSCAdmin (it's managed=False and in online_edu)
                return db == 'online_edu'
            else:
                # Migrate LSCUser and others to default database
                return db == 'default'
        
        # Route admissions app to default
        if app_label == 'admissions':
            return db == 'default'
        
        # Django default apps (admin, auth, sessions, etc) go to default
        if app_label in ['admin', 'auth', 'contenttypes', 'sessions']:
            return db == 'default'
        
        return None
