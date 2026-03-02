from django.apps import AppConfig

# --- RENAMED: from SocialappConfig to SocialAppConfig for consistency ---
class SocialAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # --- FIXED: This MUST match the folder name exactly ---
    name = 'SocialApp'

    def ready(self):
        # This part is still correct
        import SocialApp.signals

