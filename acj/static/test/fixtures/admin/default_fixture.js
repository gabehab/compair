var UserFactory = require('../../factories/user_factory.js');
var userFactory = new UserFactory();

var SessionFactory  = require('../../factories/session_factory.js');
var sessionFactory = new SessionFactory();

var storage = {
    session: {},
    users: [],
    userTypes: [
        { "id": 1, "name": "Student" }, 
        { "id": 2, "name": "Instructor" }, 
        { "id": 3, "name": "System Administrator"  }
    ]
}

var admin = userFactory.generateUser(1, "System Administrator", {
    username: "root",
    displayname: "root",
    firstname: "JaNy",
    lastname: "bwsV",
    fullname: "JaNy bwsV",
});
storage.users.push(admin);

var instructor = userFactory.generateUser(2, "Instructor", {
    username: "instructor1",
    displayname: "First Instructor",
    firstname: "First",
    lastname: "Instructor",
    fullname: "First Instructor",
    email: "first.instructor@exmple.com"
});
storage.users.push(instructor);



storage.loginDetails = { id: admin.id, username: admin.username, password: "password" };
var session = sessionFactory.generateSession(admin.id, admin.system_role, {});
storage.session = session;

module.exports = storage;