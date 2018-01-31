var UserFactory = require('../../factories/user_factory.js');
var userFactory = new UserFactory();

var SessionFactory = require('../../factories/session_factory.js');
var sessionFactory = new SessionFactory();

var CourseFactory = require('../../factories/course_factory.js');
var courseFactory = new CourseFactory();

var AssignmentFactory = require('../../factories/assignment_factory.js');
var assignmentFactory = new AssignmentFactory();

var CriterionFactory = require('../../factories/criterion_factory.js');
var criterionFactory = new CriterionFactory();

var LTIConsumerFactory = require('../../factories/lti_consumer_factory.js');
var ltiConsumerFactory = new LTIConsumerFactory();

var LTIContextFactory = require('../../factories/lti_context_factory.js');
var ltiContextFactory = new LTIContextFactory();

var LTIUserFactory = require('../../factories/lti_user_factory.js');
var ltiUserFactory = new LTIUserFactory();

var ThirdPartyUserFactory = require('../../factories/third_party_user_factory.js');
var thirdPartyUserFactory = new ThirdPartyUserFactory();

var storage = {
    session: {},
    users: {},
    courses: {},
    user_courses: {},
    groups: [],
    assignments: {},
    course_assignments: {},
    criteria: {},
    lti_consumers: {},
    lti_contexts: {},
    user_lti_users: {},
    user_third_party_users: {},
    user_search_results: {}
}

var admin = userFactory.generateUser("1abcABC123-abcABC123_Z", "System Administrator", {
    username: "root",
    displayname: "root",
    firstname: "JaNy",
    lastname: "bwsV",
    fullname: "JaNy bwsV",
    fullname_sortable: "bwsV, JaNy",
    email: "admin@exmple.com"
});
storage.users[admin.id] = admin;

var instructor = userFactory.generateUser("2abcABC123-abcABC123_Z", "Instructor", {
    username: "instructor1",
    displayname: "First Instructor",
    firstname: "First",
    lastname: "Instructor",
    fullname: "First Instructor",
    fullname_sortable: "Instructor, First",
    email: "first.instructor@exmple.com"
});
storage.users[instructor.id] = instructor;

var student1 = userFactory.generateUser("3abcABC123-abcABC123_Z", "Student", {
    username: "student1",
    displayname: "First Student",
    firstname: "First",
    lastname: "Student",
    fullname: "First Student",
    fullname_sortable: "Student, First",
    email: "first.student@exmple.com"
});
storage.users[student1.id] = student1;

var student2 = userFactory.generateUser("4abcABC123-abcABC123_Z", "Student", {
    username: "student2",
    displayname: "Second Student",
    firstname: "Second",
    lastname: "Student",
    fullname: "Second Student",
    fullname_sortable: "Student, Second",
    email: "second.student@exmple.com"
});
storage.users[student2.id] = student2;

var course = courseFactory.generateCourse("1abcABC123-abcABC123_Z",  {
    name: "CHEM 111",
    year: 2015,
    term: "Winter"
});
storage.courses[course.id] = course;

var course2 = courseFactory.generateCourse("2abcABC123-abcABC123_Z", {
    name: "PHYS 101",
    year: 2015,
    term: "Winter"
});
storage.courses[course2.id] = course2;

var group1 = "First Group";
storage.groups.push(group1);
var group2 = "Second Group";
storage.groups.push(group2);
var group3 = "Third Group";
storage.groups.push(group3);


var defaultCriterion = criterionFactory.getDefaultCriterion();
storage.criteria[defaultCriterion.id] = defaultCriterion;

var criterion2 = criterionFactory.generateCriterion("2abcABC123-abcABC123_Z", admin.id, {
    "name": "Which sounds better?",
    "description": "<p>Choose the response that you think sounds more accurate of the two.</p>",
    "default": true
});
storage.criteria[criterion2.id] = criterion2;

var criterion3 = criterionFactory.generateCriterion("3abcABC123-abcABC123_Z",  admin.id, {
    "name": "Which looks better?",
    "description": "<p>Choose the response that you think looks more accurate of the two.</p>",
    "default": false,
    "compared": true
});
storage.criteria[criterion3.id] = criterion3;

// user_courses
storage.user_courses[admin.id] = [
    { courseId: course.id, courseRole: "Instructor", groupName: group1 },
    { courseId: course2.id, courseRole: "Instructor", groupName: null }
];

storage.user_courses[student1.id] = [
    { courseId: course.id, courseRole: "Student", groupName: group1 }
];

storage.course_assignments[course.id] = [];

var assignment_finished = assignmentFactory.generateAssignment("1abcABC123-abcABC123_Z", admin, [defaultCriterion, criterion3], {
    "name": "Assignment Finished",
    "students_can_reply": true,
    "available": true,
    "compared": true,
    "compare_period": false,
    "after_comparing": true,
    "answer_period": false,
    "content": "<p>This assignment should already be completed</p>"
});
storage.assignments[assignment_finished.id] = assignment_finished;
storage.course_assignments[course.id].push(assignment_finished.id);

var assignment_being_compared = assignmentFactory.generateAssignment("2abcABC123-abcABC123_Z", admin, [defaultCriterion, criterion3], {
    "name": "Assignment Being Compared",
    "students_can_reply": true,
    "available": true,
    "compared": true,
    "compare_period": true,
    "after_comparing": false,
    "answer_period": false,
    "content": "<p>This assignment should be compared right now</p>"
});
storage.assignments[assignment_being_compared.id] = assignment_being_compared;
storage.course_assignments[course.id].push(assignment_being_compared.id);

var assignment_being_answered = assignmentFactory.generateAssignment("3abcABC123-abcABC123_Z", admin, [defaultCriterion, criterion3], {
    "name": "Assignment Being Answered",
    "students_can_reply": true,
    "available": true,
    "compared": false,
    "compare_period": false,
    "after_comparing": false,
    "answer_period": true,
    "content": "<p>This assignment should be answered right now</p>"
});
storage.assignments[assignment_being_answered.id] = assignment_being_answered;
storage.course_assignments[course.id].push(assignment_being_answered.id);

var assignment_upcoming = assignmentFactory.generateAssignment("4abcABC123-abcABC123_Z", admin, [defaultCriterion, criterion3], {
    "name": "Assignment Upcoming",
    "students_can_reply": true,
    "available": false,
    "compared": false,
    "compare_period": false,
    "after_comparing": false,
    "answer_period": false,
    "content": "<p>This assignment should be coming in the future</p>"
});
storage.assignments[assignment_upcoming.id] = assignment_upcoming;
storage.course_assignments[course.id].push(assignment_upcoming.id);

var consumer1 = ltiConsumerFactory.generateConsumer("1abcABC123-abcABC123_Z", "consumer_key_1", "consumer_secret_1", {
    "user_id_override": "consumer_user_id_override"
});
var consumer2 = ltiConsumerFactory.generateConsumer("2abcABC123-abcABC123_Z", "consumer_key_2", "consumer_secret_2");
var consumer3 = ltiConsumerFactory.generateConsumer("3abcABC123-abcABC123_Z", "consumer_key_3", "consumer_secret_3", {
    "active": false
});

storage.lti_consumers[consumer1.id] = consumer1;
storage.lti_consumers[consumer2.id] = consumer2;
storage.lti_consumers[consumer3.id] = consumer3;

var context1 = ltiContextFactory.generateContext("1abcABC123-abcABC123_Z", consumer1, course, {
    "context_id": "canvas.course.1",
    "context_title": "Canvas Course One",
});

var context2 = ltiContextFactory.generateContext("2abcABC123-abcABC123_Z", consumer1, course2, {
    "context_id": "canvas.course.2",
    "context_title": "Canvas Course Two",
});

var context3 = ltiContextFactory.generateContext("3abcABC123-abcABC123_Z", consumer2, course, {
    "context_id": "blackboard.course.2",
    "context_title": "Blackboard Course One",
});

storage.lti_contexts[context1.id] = context1;
storage.lti_contexts[context2.id] = context2;
storage.lti_contexts[context3.id] = context3;

// lti_users

var lti_user1 = ltiUserFactory.generateLTIUser("1abcABC123-abcABC123_Z", consumer1, student1, {
    "lti_user_id": "12345000001",
    "lis_person_name_full": "Student One",
    "oauth_consumer_key": 'consumer_key_1',
});

var lti_user2 = ltiUserFactory.generateLTIUser("2abcABC123-abcABC123_Z", consumer1, student1, {
    "lti_user_id": "12345000002",
    "lis_person_name_full": "Student One",
    "oauth_consumer_key": 'consumer_key_1',
});

var lti_user3 = ltiUserFactory.generateLTIUser("3abcABC123-abcABC123_Z", consumer1, student2, {
    "lti_user_id": "12345000003",
    "lis_person_name_full": "Student Two",
    "oauth_consumer_key": 'consumer_key_1',
});

storage.user_lti_users[student1.id] = [lti_user2, lti_user1];
storage.user_lti_users[student2.id] = [lti_user3];

// third_party_users

var third_party_user1 = thirdPartyUserFactory.generatethirdPartyUser("1abcABC123-abcABC123_Z", student1, {
    "third_party_type": "CAS",
    "unique_identifier": "CAS0001",
});

var third_party_user2 = thirdPartyUserFactory.generatethirdPartyUser("2abcABC123-abcABC123_Z", student1, {
    "third_party_type": "CAS",
    "unique_identifier": "CAS0002",
});

var third_party_user3 = thirdPartyUserFactory.generatethirdPartyUser("3abcABC123-abcABC123_Z", student2, {
    "third_party_type": "CAS",
    "unique_identifier": "CAS0003",
});

storage.user_third_party_users[student1.id] = [third_party_user2, third_party_user1];
storage.user_third_party_users[student2.id] = [third_party_user3];

// user_search_results
storage.user_search_results.objects = [student2];
storage.user_search_results.total = 1;

storage.loginDetails = { id: admin.id, username: admin.username, password: "password" };
var session = sessionFactory.generateSession(admin.id, admin.system_role, {});
storage.session = session;

module.exports = storage;