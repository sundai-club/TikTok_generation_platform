/**
 * Run `build` or `dev` with `SKIP_ENV_VALIDATION` to skip env validation. This is especially useful
 * for Docker builds.
 */
await import("./src/env.js");

/** @type {import("next").NextConfig} */
const config = {
    api: {
        bodyParser: {
            sizeLimit: "100mb",
        },
        responseLimit: "100mb",
    },
};

export default config;
