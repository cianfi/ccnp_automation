configure-lab:
	@echo "Configuring lab environment..."
	python build/build_cml.py
	@echo "Lab environment configured successfully."

wipe-cml-infra:
	@echo "Wiping and rebuilding the CML infrastructure lab..."
	python build/build_cml.py --replace
	@echo "CML infrastructure lab rebuilt successfully."

fix-ssh-on-jumphost:
	@echo "Pushing SSH configuration..."
	scp -r build/ssh_config developer@10.10.20.50:~/.ssh/config
	@echo "SSH configuration pushed successfully."

setup-lab:
	@echo "Setting up Lab..."
	make configure-lab
	make fix-ssh-on-jumphost
	@echo "Lab configuration successful."