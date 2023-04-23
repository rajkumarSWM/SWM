const puppeteer = require('puppeteer');                                                                                                                                                                             
const jsdom = require("jsdom")
const createCsvWriter = require('csv-writer').createObjectCsvWriter;
var fs = require("fs");

const {JSDOM} = jsdom
global.DOMParser = new JSDOM().window.DOMParser


const csvWriter = createCsvWriter({
    path: './stroke.csv',
    header: [
        {id: 'url', title: 'URL'}
    ]
});

const isHeadless = false

function delay(time) {
    return new Promise(function (resolve) {
        setTimeout(resolve, time)
    });
}

async function goToPage(page, post_url) {

    await page.goto(post_url,
        { waitUntil: 'networkidle2' })
    
    await page.waitForSelector('#pi37-paged-content')

    for (i = 0; i < 10; i++) {
        xpathExpr = '//*[@id="pi37-paged-content"]/ul/li[' + i + ']/div[2]/h3/a';
        const [element] = await page.$x(xpathExpr);
        console.log(await (await element.getProperty('href')).jsonValue());
      }

}

exports.gotopage = async function(post_url){
    pagename = "goodrx"
    const browser = await puppeteer.launch({headless: isHeadless})
    const context = browser.defaultBrowserContext();
    const page = await browser.newPage()

    await page.setViewport({width: 1280, height: 800})


    await goToPage(page, 'https://messageboards.webmd.com/health-conditions/f/stroke');

    await browser.close();
}
