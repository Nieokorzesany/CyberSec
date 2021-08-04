
const subdomainGenerator = function(length){
    const charset='abcdefghijklmnoprstuvwxyz'.split('')
    let subdomains = charset
    let subdomain
    let letter
    let temp

    for (let i = 1;i<length;i++){
        temp=[]
        for(let k=0;k<subdomains[k].length;k++){
            subdomain = subdomains[k]
            for(let j=0;j<charset.length;j++){
                letter=charset[j]
                temp.push(subdomain + letter)
            }
        }
        subdomains=temp
    }
    return subdomains
}

const test = subdomainGenerator(4)

console.log(test)