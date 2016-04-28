// Use the external Chai As Promised to deal with resolving promises in
// expectations
var chai = require('chai');
var chaiAsPromised = require('chai-as-promised');
chai.use(chaiAsPromised);

var expect = chai.expect;

var createCourseStepDefinitionsWrapper = function () {
    this.Given(/^I fill in the course description with "([^"]*)"$/, function(text, done) {
        //load the ckeditor iframe
        browser.wait(browser.isElementPresent(element(by.css("#cke_courseDescription iframe"))), 1000);
        browser.driver.switchTo().frame(element(by.css("#cke_courseDescription iframe")).getWebElement());
        // clear the content
        browser.driver.executeScript("document.body.innerHTML = '';")
        browser.driver.findElement(by.css("body")).sendKeys(text);
        browser.driver.switchTo().defaultContent();
        done();
    });
};
module.exports = createCourseStepDefinitionsWrapper;