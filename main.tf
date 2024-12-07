# providers.tf
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.0"
    }
  }
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
}

# networks.tf
resource "docker_network" "app_network" {
  name = "app_network"
}

# volumes.tf
resource "docker_volume" "mongo_data" {
  name = "mongo-data"
}

resource "docker_volume" "prometheus_data" {
  name = "prometheus-data"
}

resource "docker_volume" "grafana_data" {
  name = "grafana-data"
}

# mongodb.tf
resource "docker_image" "mongodb" {
  name = "mongo:5.0"
}

resource "docker_container" "mongodb" {
  name  = "mongodb"
  image = docker_image.mongodb.image_id

  ports {
    internal = 27017
    external = 27017
  }

  volumes {
    volume_name    = docker_volume.mongo_data.name
    container_path = "/data/db"
  }

  networks_advanced {
    name = docker_network.app_network.name
  }
}

# backend.tf
resource "docker_image" "backend" {
  name = "backend"
  build {
    context = "./backend"
  }
}

resource "docker_container" "backend" {
  name  = "backend"
  image = docker_image.backend.image_id

  ports {
    internal = 8000
    external = 8000
  }

  networks_advanced {
    name = docker_network.app_network.name
  }

  env = [
    "MONGO_DETAILS=mongodb://mongodb:27017"
  ]

  depends_on = [docker_container.mongodb]
}

# frontend.tf
resource "docker_image" "frontend" {
  name = "frontend"
  build {
    context = "./frontend"
  }
}

resource "docker_container" "frontend" {
  name  = "frontend"
  image = docker_image.frontend.image_id

  ports {
    internal = 5173
    external = 5173
  }

  networks_advanced {
    name = docker_network.app_network.name
  }

  depends_on = [docker_container.backend]
}

# ollama.tf
resource "docker_image" "ollama" {
  name = "ollama"
  build {
    context = "./ollama"
  }
}

resource "docker_container" "ollama" {
  name  = "ollama"
  image = docker_image.ollama.image_id

  ports {
    internal = 11434
    external = 11434
  }

  networks_advanced {
    name = docker_network.app_network.name
  }
}

# nginx.tf
resource "docker_image" "nginx" {
  name = "nginx:alpine"
}

resource "docker_container" "nginx" {
  name  = "nginx"
  image = docker_image.nginx.image_id

  ports {
    internal = 80
    external = 80
  }

  volumes {
    host_path      = "${path.cwd}/nginx/nginx.conf"
    container_path = "/etc/nginx/nginx.conf"
    read_only      = true
  }

  volumes {
    host_path      = "${path.cwd}/nginx/conf.d"
    container_path = "/etc/nginx/conf.d"
    read_only      = true
  }

  networks_advanced {
    name = docker_network.app_network.name
  }

  depends_on = [
    docker_container.frontend,
    docker_container.backend,
    docker_container.ollama
  ]
}

# prometheus.tf
resource "docker_image" "prometheus" {
  name = "prom/prometheus:latest"
}

resource "docker_container" "prometheus" {
  name  = "prometheus"
  image = docker_image.prometheus.image_id

  ports {
    internal = 9090
    external = 9090
  }

  volumes {
    host_path      = "${path.cwd}/prometheus"
    container_path = "/etc/prometheus"
  }

  volumes {
    volume_name    = docker_volume.prometheus_data.name
    container_path = "/prometheus"
  }

  command = [
    "--config.file=/etc/prometheus/prometheus.yml",
    "--storage.tsdb.path=/prometheus",
    "--web.console.libraries=/usr/share/prometheus/console_libraries",
    "--web.console.templates=/usr/share/prometheus/consoles"
  ]

  networks_advanced {
    name = docker_network.app_network.name
  }

  depends_on = [docker_container.backend]
}

# grafana.tf
resource "docker_image" "grafana" {
  name = "grafana/grafana:latest"
}

resource "docker_container" "grafana" {
  name  = "grafana"
  image = docker_image.grafana.image_id

  ports {
    internal = 3000
    external = 3000
  }

  volumes {
    volume_name    = docker_volume.grafana_data.name
    container_path = "/var/lib/grafana"
  }

  volumes {
    host_path      = "${path.cwd}/grafana/provisioning"
    container_path = "/etc/grafana/provisioning"
  }

  env = [
    "GF_SECURITY_ADMIN_PASSWORD=admin",
    "GF_SECURITY_ADMIN_USER=admin"
  ]

  networks_advanced {
    name = docker_network.app_network.name
  }

  depends_on = [docker_container.prometheus]
}

# node-exporter.tf
resource "docker_image" "node_exporter" {
  name = "prom/node-exporter:latest"
}

resource "docker_container" "node_exporter" {
  name  = "node-exporter"
  image = docker_image.node_exporter.image_id

  ports {
    internal = 9100
    external = 9100
  }

  volumes {
    host_path      = "/proc"
    container_path = "/host/proc"
    read_only      = true
  }

  volumes {
    host_path      = "/sys"
    container_path = "/host/sys"
    read_only      = true
  }

  volumes {
    host_path      = "/"
    container_path = "/rootfs"
    read_only      = true
  }

  command = [
    "--path.procfs=/host/proc",
    "--path.sysfs=/host/sys",
    "--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)"
  ]

  networks_advanced {
    name = docker_network.app_network.name
  }
}
