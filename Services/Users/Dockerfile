FROM golang:1.19.0-alpine3.15 AS builder
RUN apk add --no-cache git gcc musl-dev
WORKDIR /go/src/app
COPY . .
RUN go mod download
RUN go build -o /go/bin/app 

FROM alpine:3.15.0
RUN apk add --no-cache ca-certificates
COPY --from=builder /go/bin/app /app
COPY --from=builder /go/src/app/*.db /
ENTRYPOINT /app
LABEL Name=UsersServer Version=0.0.1
EXPOSE 4052
CMD ["users_service"]


