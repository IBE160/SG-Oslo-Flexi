from typing import Optional
from redis import Redis
from rq import Queue
from app.schemas.orchestrator import ConversationContext, WorkflowState
from app.workers.tasks import process_ocr_task
from app.services.reader_agent import ReaderAgent

class Orchestrator:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client
        self.queue = Queue(connection=redis_client)
        # Placeholder for the agent
        self.reader_agent = ReaderAgent()

    def load_context(self, session_id: str) -> Optional[ConversationContext]:
        data = self.redis.get(f"session:{session_id}")
        if data:
            return ConversationContext.model_validate_json(data)
        return None

    def save_context(self, context: ConversationContext):
        self.redis.set(f"session:{context.session_id}", context.model_dump_json())

    def update_state(self, session_id: str, new_state: WorkflowState) -> Optional[ConversationContext]:
        context = self.load_context(session_id)
        if context:
            context.state = new_state
            self.save_context(context)
            # Check if this state transition should trigger a new action
            self.trigger_next_step(context)
            return context
        return None

    def create_instance(self, session_id: str) -> ConversationContext:
        context = ConversationContext(session_id=session_id, state=WorkflowState.UPLOADED)
        self.save_context(context)
        return context

    def start_workflow(self, session_id: str) -> ConversationContext:
        """
        Initializes the workflow and triggers the first step.
        """
        context = self.create_instance(session_id)
        self.trigger_next_step(context)
        return context

    def trigger_next_step(self, context: ConversationContext):
        """
        Decides the next action based on the current state.
        """
        if context.state == WorkflowState.UPLOADED:
            # Transition to PROCESSING/OCR
            # In a real app, we might check if the file is ready, etc.
            self.update_state_internal_only(context, WorkflowState.OCR)
            self.queue.enqueue(process_ocr_task, context.session_id)
        
        elif context.state == WorkflowState.OCR_COMPLETED:
            # After OCR, transition to the analysis state
            self.update_state_internal_only(context, WorkflowState.ANALYZING)
            # Directly call the Reader Agent
            updated_context = self.reader_agent.process(context)
            self.save_context(updated_context)
            self.update_state_internal_only(updated_context, WorkflowState.ANALYZED)

        elif context.state == WorkflowState.ANALYZED:
            # Maybe trigger a final completion step or notification
            self.update_state_internal_only(context, WorkflowState.COMPLETED)
    
    def update_state_internal_only(self, context: ConversationContext, new_state: WorkflowState):
        """
        Updates state without triggering side effects (recursion prevention).
        """
        context.state = new_state
        self.save_context(context)
