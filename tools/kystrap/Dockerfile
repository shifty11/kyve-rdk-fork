# Build stage
FROM golang:1.22.0-alpine AS build

# Set work directory
WORKDIR /app

# Copy go mod/sum files and download dependencies
COPY go.mod go.sum ./
RUN go mod download

# Copy source files
COPY bootstrap ./bootstrap
COPY cmd ./cmd
COPY grpcall ./grpcall
COPY types ./types
COPY main.go ./

# Build the Go app
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o kystrap .

# Final stage to run the binary
FROM alpine:latest

# Set work directory
WORKDIR /app

# Copy the binary from the build stage
COPY --from=build /app/kystrap .

# Copy the template files
COPY ./templates /app/templates
COPY ./template-strings.yml /app/template-strings.yml
COPY ./protobuf.descriptor.bin /app/protobuf.descriptor.bin

ENTRYPOINT ["./kystrap"]
