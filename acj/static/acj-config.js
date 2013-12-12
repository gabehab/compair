var myApp = angular.module('myApp', ['flash', 'ngRoute', 'ngResource', 'ngTable', 'http-auth-interceptor', 'ngCookies', 'ngUpload', '$strap.directives']);

//Global Variables

myApp.factory('installService', function($resource) {
	return $resource('/install');
});

myApp.factory('createAdmin', function($resource) {
	return $resource( '/admin' );
});

myApp.factory('isInstalled', function($resource) {
	return $resource( '/isinstalled' );
});

myApp.factory('judgeService', function($resource) {
	return $resource( '/script/:scriptId' );
});

myApp.factory('loginService', function($resource) {
	return $resource( '/login' );
});

myApp.factory('logoutService', function($resource) {
	return $resource( '/logout' );
});

myApp.factory('roleService', function($resource) {
	return $resource( '/roles' );
});

myApp.factory('userService', function($resource) {
	return $resource( '/user/:uid', {}, { put: {method: 'PUT'} } );
});

myApp.factory('allUserService', function($resource) {
	return $resource( '/allUsers' );
});

myApp.factory('pickscriptService', function($resource) {
	return $resource( '/pickscript/:qid/:sidl/:sidr', {sidl: 0, sidr: 0} );
});

myApp.factory('rankService', function($resource) {
	return $resource( '/ranking/:qid' );
});

myApp.factory('courseService', function($resource) {
	return $resource( '/course' );
});

myApp.factory('editcourseService', function($resource) {
	return $resource( '/editcourse/:cid', {}, { put: {method: 'PUT'} } );
});

myApp.factory('questionService', function($resource) {
	return $resource( '/question/:cid', {}, { put: {method: 'PUT'} } );
});

myApp.factory('answerService', function($resource) {
	return $resource( '/answer/:qid', {}, { put: {method: 'PUT'} } );
});

myApp.factory('quickService', function($resource) {
	return $resource( '/randquestion' );
});

myApp.factory('enrollService', function($resource) {
	return $resource( '/enrollment/:id', {}, { put: {method: 'PUT'} } );
});

myApp.factory('commentAService', function($resource) {
	return $resource( '/answer/:id/comment', {}, { put: {method: 'PUT'} } );
});

myApp.factory('commentQService', function($resource) {
	return $resource( '/question/:id/comment', {}, { put: {method: 'PUT'} } );
});

myApp.factory('commentJService', function($resource) {
	return $resource( '/judgepage/:id/comment/:sidl/:sidr', {}, { put: {method: 'PUT'} } );
});

myApp.factory('passwordService', function($resource) {
	return $resource( '/password/:uid' );
});

myApp.factory('reviewjudgeService', function($resource) {
	return $resource( '/judgements/:qid' );
});

myApp.factory('notificationService', function($resource) {
	return $resource( '/notifications' );
});

myApp.factory('critService', function($resource) {
	return $resource( '/managecategories/:cid/:critid' );
});

myApp.factory('tagService', function($resource) {
	return $resource( '/managetag/:cid/:tid' );
});

myApp.factory('statisticService', function($resource) {
	return $resource( '/statistics/:cid' );
});

myApp.factory('statisticExportService', function($resource) {
	return $resource( '/statisticexport/', {}, { put: {method: 'POST'} } );
});

//used for testing
myApp.factory('resetDB', function($resource) {
	return $resource( '/resetdb' );
});

myApp.factory('flashService', function(flash) {
	return {
		flash: function (type, msg) {
			type = 'alert alert-' + type + ' text-center';
			flash([{ level: type, text: msg}]);
		}		
	};
});

myApp.config( function ($routeProvider) {
	$routeProvider
		.when ('/install', 
			{
				controller: InstallController,
				templateUrl: 'install.html'
			})
		.when ('/install2', 
			{
				controller: InstallController,
				templateUrl: 'install2.html'
			})
		.when ('/', 
			{
				controller: CourseController,
				templateUrl: 'coursepage.html'
			})
		.when ('/judgepage/:questionId',
			{
				controller: JudgepageController,
				templateUrl: 'judgepage.html'
			})
		.when ('/login',
			{
				controller: LoginController,
				templateUrl: 'login.html'
			})
		.when ('/createuser',
			{
				controller: UserController,
				templateUrl: 'createuser.html'
			})
		.when ('/user',
			{
				controller: UserIndexController,
				templateUrl: 'userpage.html'
			})
//		.when ('/rankpage',
//			{
//				controller: RankController,
//				templateUrl: 'rankpage.html'
//			})
		.when ('/questionpage/:courseId',
			{
				controller: QuestionController,
				templateUrl: 'questionpage.html'
			})
		.when ('/answerpage/:questionId',
			{
				controller: AnswerController,
				templateUrl: 'answerpage.html'
			})
		.when ('/enrollpage/:courseId',
			{
				controller: EnrollController,
				templateUrl: 'enrollpage.html'
			})
		.when ('/quickjudge',
			{
				controller: QuickController,
				templateUrl: 'judgepage.html'
			})
		.when ('/userprofile/:userId',
			{
				controller: ProfileController,
				templateUrl: 'userprofile.html'
			})
		.when('/classimport',
			{
				controller: ImportController,
				templateUrl: 'classimport.html'
			})
		.when ('/reviewjudge/:qid',
			{
				controller: ReviewJudgeController,
				templateUrl: 'reviewjudge.html'
			})
		.when ('/editcourse/:courseId',
			{
				controller: EditCourseController,
				templateUrl: 'editcourse.html'
			})
		.when ('/stats/:courseId',
			{
				controller: StatisticController,
				templateUrl: 'stats.html'
			})
		.when ('/statexport/:cid/:cname',
				{
			controller: StatisticExportController,
			templateUrl: 'statexport.html'
			})
		.otherwise({redirectTo: '/'});
});