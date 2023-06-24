
async function getDate() {
    const dt = new Date();
    dt.setHours(dt.getHours() + 7);
    return dt.toISOString().replace("T", " ").replace("Z", "").split(".")[0]
}

let last_biggest_name_length = 0;
async function __log(level: string, name: string, ...args: Array<any>) {
    if(name.length > last_biggest_name_length) last_biggest_name_length = name.length;
    getDate().then(async date => {
        console.log("[" + date + "][" + level.padStart(5, " ") + "]" + "[" + name.padStart(last_biggest_name_length, " ") + "]", ...args);
    });
}

async function debug(name: string, ...args: Array<any>) {
    __log("DEBUG", name, ...args);
}

async function log(name: string, ...args: Array<any>) {
    __log("INFO", name, ...args);
}

async function error(name: string, ...args: Array<any>) {
    __log("ERROR", name, ...args);
}

export const DEBUGGER = {
    debug,
    log,
    error
}