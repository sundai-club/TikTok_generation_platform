const ignoreWatchList = [
  "*.md",
  "scratch*",
  "src/scratch*",
  "node_modules",
  "!node_modules/.prisma",
  "src/app",
  "*.py",
  ".git",
  ".next",
  "tsconfig.tsbuildinfo",
];

module.exports = {
  apps: [
    {
      name: "redis",
      script: "sudo -u redis redis-server /etc/redis/redis.conf",
      time: true,
    },
    {
      name: "postgres",
      script:
        "sudo -u postgres /usr/lib/postgresql/15/bin/postgres --config-file=/etc/postgresql/15/main/postgresql.conf",
      time: true,
    },
    {
      name: "app",
      script: "npx tsx ./src/scripts/run.ts",
      watch: false,
      ignore_watch: ignoreWatchList,
      time: true,
    },
    // {
    //   name: "code-server",
    //   script: `bash -c '
    //       code-server --install-extension bradlc.vscode-tailwindcss
    //       code-server --install-extension dsznajder.es7-react-js-snippets
    //       code-server --install-extension ms-python.python
    //       code-server --install-extension Prisma.prisma
    //       code-server --install-extension dbaeumer.vscode-eslint
    //       code-server --install-extension esbenp.prettier-vscode
    //       code-server --install-extension mhutchie.git-graph
    //       code-server --bind-addr 0.0.0.0:8003 --auth none --cert false /opt/app
    //     '`,
    //   time: true,
    // },
    {
      name: "cron",
      script: "cron -f",
      time: true,
    },
    {
      name: "nginx",
      script: "nginx -g 'daemon off;'",
      time: true,
    },
    {
      name: "adminer",
      script: "php -S 0.0.0.0:8004 /opt/app/.devops/adminer-custom.php",
      time: true,
    },
  ],
};
