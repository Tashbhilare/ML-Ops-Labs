provider "google" {
    project = "terraform-lab-tanish"
    region  = "us-central1"
    zone    = "us-central1-a"
}

resource "google_compute_instance" "vm_instance" {
    name         = "terraform-vm"
    machine_type = "e2-micro"
    zone         = "us-central1-a"
    allow_stopping_for_update = true

    labels = {
        environment = "development"
        owner       = "team-terraform"
    }

    boot_disk {
        initialize_params {
            image = "debian-cloud/debian-11"
            size  = 12
        }
    }

    network_interface {
        network = "default"
    }
}

resource "google_storage_bucket" "terraform_lab_bucket" {
    name          = "terraform-lab-bucket-tanish-2026"
    location      = "us-central1"
    force_destroy = true
}
