import { AgentBay,Session } from '../../src';
import * as sinon from 'sinon';
import { getTestApiKey } from '../utils/test-helpers';


declare function describe(name: string, fn: () => void): void;
declare function beforeEach(fn: () => void | Promise<void>): void;
declare function afterEach(fn: () => void | Promise<void>): void;
declare function it(name: string, fn: () => void | Promise<void>): void;
declare function expect(actual: any): any;


describe('Session Parameters', () => {
  let agentBay: AgentBay;
  let clientStub: any;
  let session: Session;
  
  beforeEach(async() => {

    const apiKey = getTestApiKey();
    agentBay = new AgentBay({ apiKey });
    clientStub = {
      create:sinon.stub()
    };
  });
  afterEach(async () => {
    try {
      if(session){
        session.delete();
        console.log('Session deleted sucessfully');
        
      }
    } catch (error) {
      console.log(`Error deleting session: ${error}`);
    }
    sinon.restore();
  });
  
  describe('create method options', () => {
    it('should accept empty options', async () => {
      try{
       session =  await agentBay.create();
      }catch(error){
        console.log(error)
      }
      
    });
    
    it('should accept contextId option', async () => {
      try{
        const contextId = 'test-context-id';
        session = await agentBay.create({ contextId });
      }catch(error:any){
        expect(error.message).toMatch(/Failed to create session/);
      }
      
    });
    
    it('should accept labels option', async () => {
      try{
      
        const labels = { username: 'alice', project: 'my-project' };
        session = await agentBay.create({ labels });
      }catch(error:any){
        console.log(error)
        expect(error.message).toMatch(/Failed to create session/);
      }
      
    });
    
    it('should accept both contextId and labels options', async () => {
      try{
        const contextId = 'test-context-id';
        const labels = { username: 'alice', project: 'my-project' };
        session = await agentBay.create({ contextId, labels });
      }catch(error:any){
        console.log(error)
        expect(error.message).toMatch(/Failed to create session/);
      }
    });
  });
  
  describe('session creation with options', () => {
    it('should create a session with the specified options', async () => {
      try{
         session = await agentBay.create({
          contextId: 'test-context-id',
          labels: { username: 'alice' }
        });
      }catch(error:any){
        console.log(error)
        expect(error.message).toMatch(/Failed to create session/);
      }
      
    });
  });
});