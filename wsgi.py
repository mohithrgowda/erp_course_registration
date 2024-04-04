from main import app
#import os

if __name__ == "__main__":
  #port = int(os.environ.get("PORT", 80))
  app.secret_key = 'PESERP'
  app.config['SESSION_TYPE'] = 'filesystem'
  app.jinja_env.cache = {}
  app.run(debug=True)
