## Test Strategy Document

Team - PepeD

            Kaveesha Nissanka ()

            Sadeeptha Bandara (30769140)


[TOC]



### Scope

This Project is on developing and testing an application that uses the Google Calendar API, that is able to access the Google Calendar of a user and perform certain tasks. Development is done concurrently with testing and focuses on getting a set of discrete functionality done.

This document will outline the testing process followed and how tests will be generally formulated. 

As the project is relatively small scale, this test strategy will be reviewed and approved by both team members. 


### Test approach

Given the nature of this application, testing is <span style="text-decoration:underline;">primarily at the Unit Testing Level</span>, as the application is developed as chunks of functionality, rather than an integrated whole.

Testing will be approached by using whitebox and blackbox testing techniques to write test cases, relevant to the functionality of each user story provided.

Further, random testing will be done where applicable, and coverage testing will be done to cover all possible paths of logic in the code.

Therefore, the testing techniques used


<table>
  <tr>
   <td>Blackbox testing
   </td>
   <td>Category Partitioning
<p>
Equivalence Partitioning
<p>
Boundary Value Analysis
   </td>
  </tr>
  <tr>
   <td>Whitebox testing
   </td>
   <td>Coverage testing : Statement Coverage,          
<p>
                              Branch coverage, 
<p>
                              Condition Coverage
<p>
 
<p>
To reduce the number of redundant test cases, MC/DC will be performed on the Decision branches identified.
   </td>
  </tr>
</table>


When generating test cases, our workflow will attempt to follow,



1. Attempt to devise blackbox tests for the given scenario

           This will help to decide on all the tests to verify that the requirement is being met

2. Implementing test cases/ Implementing the program

           Based on how comfortable the team member is with the test, it chosen whether to write the test first, or implement the functionality first

3. Look at the specific implementation details of the functionality and decide if any tests are required to test that specific implementation, if there are, implementing them.
4. Performing coverage testing on the implementation, to check if all branches of logic are covered.
5. Fixing bugs if CI build fails, and modifying the CI to be upto date to the latest configuration requirements, for the application to run.

Where needed, various test environments can be created and the individual modules will be tested while they are being implemented.

Using the GitLab docker instance, continuous integration will ensure that** regression tests **are conducted, ensuring that new functionality does not break old code.


### Testing Tools

In following the test approach above, the testing tools used, will involve the following.


#### <span style="text-decoration:underline;">Testing framework</span>

**Unittest**:


    The testing framework used, will be Unittest, which comes by default, with standard Python installation. Different capabilities within this library, including mocking, patching, creating test suites, and test fixtures, will be used.

    

The unittest testing framework will be used to create unit tests, to test individual modules, while to consider testing when external dependencies are involved, Mocking will be used.

**Mock testing** will simulate API calls, allowing a variety of possible branches of the code logic to be explored. 


#### <span style="text-decoration:underline;">Continuous Integration</span>

Testing will be integrated with development and will be automated, when pushing to the relevant repository. Continuous Integration is performed on the **GitLab docker instance**, upon each push. 


#### <span style="text-decoration:underline;">Coverage Testing</span>

Further, to perform coverage testing, the open source module** coverage.py** will be used.  It will be used to generate html reports of the degree to which code is covered by the test cases.


### Roles and Responsibilities of Team members

Both team members will develop and test the application


<table>
  <tr>
   <td>Sadeeptha Bandara
   </td>
   <td>Developer
<p>
Tester
   </td>
   <td>Developing and testing the first two user stories
<p>
Managing the GitLab CI configuration, Coverage Testing
   </td>
  </tr>
  <tr>
   <td>Kaveesha Nissanka
   </td>
   <td>Developer
<p>
Tester
   </td>
   <td>Developing and testing the last two user stories.
<p>
Creating the console based UI 
   </td>
  </tr>
</table>



### Test Environment

This section describes the test environment setup, when conducting the tests. The requirements of this application all require the use of an API, to gain access to external data. (Calendar of a specific user)

**Therefore, in the view that all test cases must be independent, each test case will run after setting up a mock for the calendar API, for that specific test**.

All related mocks will be torn down, after a given test ends.

Testing will sometimes be performed in a virtual environment in Python


### Risk Analysis of possible risks that can occur when testing


<table>
  <tr>
   <td>Risk
   </td>
   <td>Severity
   </td>
   <td>Likelihood
   </td>
   <td>Mitigation Plan
   </td>
  </tr>
  <tr>
   <td>Inability to import modules
   </td>
   <td>8/10
   </td>
   <td>5/10
   </td>
   <td>Consult with the lecturer and tutors, google possible solutions. 
   </td>
  </tr>
  <tr>
   <td>Wrong interpretation of requirements, resulting in misguided test cases
   </td>
   <td>9/10
   </td>
   <td>3/10
   </td>
   <td>Review the requirements thoroughly, and reach a team consensus on what each of the requirements mean. Create test cases based on this.
<p>
Consult the tutor, if there is any serious doubt
   </td>
  </tr>
  <tr>
   <td>Scheduling issues resulting in the project being delayed 
   </td>
   <td>3/10
   </td>
   <td>4/10
   </td>
   <td>Plan ahead and decide on a common meeting time, at regular intervals.
<p>
Frequent communication between team members, so that everyone’s on the same page
   </td>
  </tr>
  <tr>
   <td>Wasting time by adding unnecessary features
   </td>
   <td>4/10
   </td>
   <td>1/10
   </td>
   <td>Stay on task and focus on the core requirements of the assignment.
   </td>
  </tr>
</table>



### Review and Approvals

All test cases will be reviewed by the team members and will be checked as to whether they adhere to the specified requirements. 

In reviewing a test case, the conditions that would be checked for, are



*   Is whether the test case is repetitive (whether previous tests cover the same logic)

	If so, MC/DC will be applied to reduce the number of test cases



*   Whether the test case is reasonable and relevant to the requirement being tested
*   Whether the test case adequately uses the Mocking and patching techniques.