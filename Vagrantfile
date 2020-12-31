# -*- mode: ruby -*-
# vi: set ft=ruby :

N = 2
Vagrant.configure("2") do |config|
    (1..N).each do |i|
        config.vm.define "node-#{i}" do |node|
            node.vm.box = "generic/ubuntu1604"
            node.vm.hostname = "node-#{i}"
            # Bridged network
            # node.vm.network "public_network", bridge: "en0: Wi-Fi (AirPort)", ip:"192.168.0.11#{i}"
            node.vm.network :private_network, ip: "192.168.0.11#{i}"
            node.vm.network "forwarded_port", guest: 8500, host: 8500 + i, auto_correct: true
            # Provider-specific configuration
            node.vm.provider "virtualbox" do |vb|
                # Customize the amount of memory on the VM
                vb.memory = "2048"
                # Specify machine name
                vb.name = "hashistack_node-#{i}"

            # Enable root passwordless by default and use same key for all nodes
            node.ssh.forward_agent = true
            node.ssh.insert_key = false
            end
        end
    end
end
