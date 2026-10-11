import {canSelfRegister} from "./studioAccessPolicy";
describe("TAP Studio private workspace access",()=>{
 it("denies anonymous public signup by default",()=>{
  expect(canSelfRegister()).toBe(false);
 });
});
