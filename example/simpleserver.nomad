job "simple-server-[[.environment_slug]]" {
  datacenters = ["lab"]
  type = "service"
  # meta {
  #   git_sha = "[[.git_sha]]"
  # }
  group "simpleserver-[[.environment_slug]]" {
    count = 1
    restart {
      attempts = 10
      interval = "5m"
      delay = "25s"
      mode = "delay"
    }
    ephemeral_disk {
      size = 300
      sticky = true
      migrate = true
    }

    task "httpserver0-[[.environment_slug]]" {
      driver = "docker"

      config {
        image = "[[.docker_image]]"
        command = "python3"
        args = [
          "-m",
          "http.server",
          "8000"
        ]
        port_map {
          http = 8000
        }
        dns_servers = [
          "consul.service.lab.consul"
        ]
        work_dir = "/var/www/html/"
      }

      resources {
        network {
          mbits = 1
          port "http" {
            static = 8000
          }
        }
      }

      service {
        name = "httpserver0-[[.environment_slug]]"
        tags = [
          "traefik.tags=service",
          "traefik.frontend.rule=PathPrefixStrip:/0/",
          //"traefik.frontend.rule=Host:[[.deploy_url]]",
        ]
        port = "http"
        check {
          name     = "alive"
          type     = "tcp"
          port     = "http"
          interval = "10s"
          timeout  = "2s"
        }
      }

      # Show both interpolated variable and nomad attribute
      env {
        DC      = "${node.datacenter}"
        VERSION = "${NOMAD_META_VERSION}"
      }

    }
  }
}
