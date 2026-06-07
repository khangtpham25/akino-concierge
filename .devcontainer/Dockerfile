FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Ho_Chi_Minh
ENV SHELL=/bin/zsh

# 1. Generate Locales and Timezone FIRST before validating environment variables
RUN apt-get update && apt-get install -y \
    tzdata \
    locales \
    && ln -sf /usr/share/zoneinfo/Asia/Ho_Chi_Minh /etc/localtime \
    && echo "Asia/Ho_Chi_Minh" > /etc/timezone \
    && sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
    && locale-gen \
    && rm -rf /var/lib/apt/lists/*

ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8
ENV PATH="/home/vscode/.local/bin:${PATH}"

# 2. Create the non-root 'vscode' user with Zsh default shell and sudo capabilities
RUN apt-get update && apt-get install -y sudo \
    && groupadd --gid 1000 vscode \
    && useradd --uid 1000 --gid 1000 -m -s /bin/zsh vscode \
    && sed -i 's|/bin/sh|/bin/zsh|g' /etc/passwd \
    && echo "vscode ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/vscode \
    && chmod 0440 /etc/sudoers.d/vscode \
    && rm -rf /var/lib/apt/lists/*

# 3. Consolidated Core Tools + PySide6 Display Dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    zsh \
    fzf \
    build-essential \
    libpq-dev \
    libgl1 \
    libglib2.0-0 \
    libxcb-xinerama0 \
    && rm -rf /var/lib/apt/lists/*

# 4. Install Oh My Zsh and plugins (Mirrored for both root and vscode users)
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended \
    && git clone https://github.com/zsh-users/zsh-autosuggestions /root/.oh-my-zsh/custom/plugins/zsh-autosuggestions \
    && git clone https://github.com/zsh-users/zsh-completions /root/.oh-my-zsh/custom/plugins/zsh-completions \
    && cp -R /root/.oh-my-zsh /home/vscode/.oh-my-zsh \
    && chown -R vscode:vscode /home/vscode/.oh-my-zsh

# Copy your custom configuration to both shell landing homes
COPY .devcontainer/.zshrc /root/.zshrc
COPY .devcontainer/.zshrc /home/vscode/.zshrc
RUN chown vscode:vscode /home/vscode/.zshrc

# 5. Global Python tool
RUN pip install uv ruff mypy pre-commit

WORKDIR /workspace

# Switch context to the non-root user matching your host's UID
USER vscode

CMD ["zsh"]
