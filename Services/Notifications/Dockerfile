FROM golang:1.19.0-alpine3.15 AS builder
RUN apk add --no-cache git gcc musl-dev
WORKDIR /go/src/app
COPY . .
RUN go mod download
RUN go build -o /go/bin/app 

FROM alpine:3.15.0
ENV TZ=America/Mexico_City
RUN apk add --no-cache ca-certificates
COPY --from=builder /go/bin/app /app
RUN mkdir events_db
ENTRYPOINT /app
LABEL Name=BonhartNotificationServer Version=1
EXPOSE 4054
CMD ["notifications_service"]


