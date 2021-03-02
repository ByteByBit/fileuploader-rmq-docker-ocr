FROM nginx:1.17-alpine

# Use custom config file.
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d