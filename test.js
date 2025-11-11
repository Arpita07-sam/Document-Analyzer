const { Builder } = require("selenium-webdriver");

(async () => {
    let driver = await new Builder().forBrowser("chrome").build();
    await driver.get("https://google.com");

    console.log(await driver.getTitle());
    await driver.quit();

})();