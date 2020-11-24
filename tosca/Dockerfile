FROM tomcat:9.0.40-jdk11

COPY ./api/target/bug-predictor-api.war /usr/local/tomcat/webapps/bug-predictor-api.war
EXPOSE 8080
ENV graphdb http://graph-db:7200

# Add docker-compose-wait tool -------------------
ENV WAIT_VERSION 2.7.3
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /wait
RUN chmod +x /wait

CMD ["catalina.sh","run"]
