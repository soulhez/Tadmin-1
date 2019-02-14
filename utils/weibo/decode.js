function decode(a) {
    var b, c, d, e, f, g, h, i = new Array((-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),(-1),62,(-1),(-1),(-1),63,52,53,54,55,56,57,58,59,60,61,(-1),(-1),(-1),(-1),(-1),(-1),(-1),0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,(-1),(-1),(-1),(-1),(-1),(-1),26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,(-1),(-1),(-1),(-1),(-1));
    for (g = a.length,
             f = 0,
             h = ""; f < g; ) {
        do
            b = i[255 & a.charCodeAt(f++)];
        while (f < g && b == -1);if (b == -1)
            break;
        do
            c = i[255 & a.charCodeAt(f++)];
        while (f < g && c == -1);if (c == -1)
            break;
        h += String.fromCharCode(b << 2 | (48 & c) >> 4);
        do {
            if (d = 255 & a.charCodeAt(f++),
                61 == d)
                return h;
            d = i[d]
        } while (f < g && d == -1);if (d == -1)
            break;
        h += String.fromCharCode((15 & c) << 4 | (60 & d) >> 2);
        do {
            if (e = 255 & a.charCodeAt(f++),
                61 == e)
                return h;
            e = i[e]
        } while (f < g && e == -1);if (e == -1)
            break;
        h += String.fromCharCode((3 & d) << 6 | e)
    }
    return h
}

function img(c) {
    var str=""
    for (var d, e, f, g, h = c[0], i = c[1], j = c.slice(2),  l = 160, m = 160, n = 0; n < j.length; n++)
        e = l / h,
        f = m / i,
        g =  j[n] % h * e + " " + parseInt(j[n] / h) * f,
        str += g+";";
    return str
}
function getimgpx(str) {
    c = decode(str).split('_');
    return img(c)
}

seed="()*,-./0123456789:?@ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnop~$^!|"
function numberTransfer(a) {
    for (var b = this.seed, c = b.substr(0, b.length - 3), d = c.length, e = b.substr(-2, 1), f = b.substr(-3, 1), g = a < 0 ? f : "", a = Math.abs(a), h = parseInt(a / d), i = [a % d]; h; )
        g += e,
        i.push(h % d),
        h = parseInt(h / d);
    for (var j = i.length - 1; j >= 0; j--)
        g += 0 == j ? c.charAt(i[j]) : c.charAt(i[j] - 1);
    return a < 0 && (g = f + g),
    g
}
function arrTransfer(a) {
    for (var b = [a[0]], c = 0; c < a.length - 1; c++) {
        for (var d = [], e = 0; e < a[c].length; e++)
            d.push(a[c + 1][e] - a[c][e]);
        b.push(d)
    }
    return b
}


function encode(a) {
    a = JSON.parse(a)
    for (var b = seed.substr(-1), c = arrTransfer(a), d = [], e = [], f = [], g = 0; g < c.length; g++)
        d.push(numberTransfer(c[g][0])),
        e.push(numberTransfer(c[g][1])),
        f.push(numberTransfer(c[g][2]));
    return d.join("") + b + e.join("") + b + f.join("")
}

function pencode(a) {
    b = a.split('%%')[1]
    a = a.split('%%')[0]
            for (var c = b.length - 2, d = b.slice(c), e = [], f = 0; f < d.length; f++) {
                var g = d.charCodeAt(f);
                e[f] = g > 57 ? g - 87 : g - 48
            }
            d = c * e[0] + e[1];
            var h, i = parseInt(a) + d, j = b.slice(0, c), k = [20, 50, 200, 500], l = [], m = {}, n = 0;
            f = 0;
            for (var o in k)
                l.push([]);
            for (var p = j.length; p > f; f++)
                h = j.charAt(f),
                m[h] || (m[h] = 1,
                l[n].push(h),
                n++,
                n == l.length && (n = 0));
            for (var q, r = i, s = "", t = k.length - 1; r > 0 && !(t < 0); )
                r - k[t] >= 0 ? (q = parseInt(Math.random() * l[t].length),
                s += l[t][q],
                r -= k[t]) : t -= 1;
            return s
        }