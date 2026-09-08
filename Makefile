configure-lab:
	@echo "Configuring lab environment..."
	python build/build_cml.py
	@echo "Lab environment configured successfully."

fix-ssh-on-jumphost:
	@echo "Pushing SSH configuration..."
	scp -r build/ssh_config developer@10.10.20.50:~/.ssh/config
	@echo "SSH configuration pushed successfully."

setup-jumphost:
	@echo "Setting up Jumphost..."
	make copy-terraform-to-jumphost
	make fix-ssh-on-jumphost
	@echo "Jumphost configuration successful."