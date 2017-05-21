Require User Login

Replace 'public' http authentication by 'user',
except for / and /web/login, and some hardcoded css, js and images
needed for our home page.

REM: web pages without authentication (auth='none') like /web/database/manager
will still be accessible without login.
