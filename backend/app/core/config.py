from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    app_name: str = 'Little Wok Story API'
    app_env: str = 'development'
    app_debug: bool = True
    app_url: str = 'http://localhost:8000'
    frontend_url: str = 'http://localhost:3000'

    database_url: str = 'postgresql+psycopg2://postgres:postgres@localhost:5432/little_wok_story'

    jwt_secret: str = 'replace-me'
    jwt_algo: str = 'HS256'
    jwt_exp_minutes: int = 60 * 24

    razorpay_key_id: str = ''
    razorpay_key_secret: str = ''
    stripe_secret_key: str = ''
    stripe_webhook_secret: str = ''

    smtp_host: str = ''
    smtp_port: int = 587
    smtp_user: str = ''
    smtp_password: str = ''
    mail_from: str = 'hello@littlewokstory.com'

    allowed_origins: str = 'http://localhost:3000'


settings = Settings()
