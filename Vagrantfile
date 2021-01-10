# -*- mode: ruby -*-
# vi: set ft=ruby :

$script = <<-SCRIPT
echo "[*] Prepare node for external Ansible provisioning..."

echo "[+] Add insecure_key to root..."
mkdir /root/.ssh && sudo cp .ssh/authorized_keys /root/.ssh

echo "[+] Install Go..."
wget https://golang.org/dl/go1.15.6.linux-amd64.tar.gz
tar -C /usr/local -xzf go1.15.6.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
echo "$(go version)"

echo "[+] Install levant..."
curl -L https://github.com/hashicorp/levant/releases/download/0.2.8/linux-amd64-levant -o /usr/local/bin/levant
chmod 755 /usr/local/bin/levant

SCRIPT

# ("2") is Vagrant version and NOT number of instances
Vagrant.configure("2") do |config|
    vm_name=['node-1','node-2']
    vm_name.each_with_index do |n,i|
        config.vm.define "#{n}" do |node|
            node.vm.box = "generic/ubuntu1604"
            node.vm.hostname = "#{n}"
            node.vm.provision "shell", inline: $script
            # Bridged network
            # node.vm.network "public_network", bridge: "en0: Wi-Fi (AirPort)", ip:"192.168.0.11#{i}"
            node.vm.network :private_network ,ip: "192.168.122.11#{i+1}"
            node.vm.network "forwarded_port", guest: 8500, host: 8500 + i + 1, auto_correct: true
            # Provider-specific configuration
            node.vm.provider :libvirt do |lv|
                # Customize the amount of memory on the VM
                lv.memory = "2048"
                lv.cpus = "2"
   
            # Enable root passwordless by default and use same key for all nodes
            node.ssh.forward_agent = true
            node.ssh.insert_key = false

            # NFS client requires adhustments in ufw, use rsync for simplicity
            if "#{n}" == 'node-1' then
                node.vm.synced_folder "example/", "/home/vagrant/example", type: "rsync",
                    sync__args: ["--verbose", "--rsync-path='sudo rsync'", "--archive", "--delete", "-z"]
            end
            end
        end
    end
end
