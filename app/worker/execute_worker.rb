class ExecuteWorker
  include Sidekiq::Worker
  sidekiq_options retry: false

  def perform
    __command = `firefox`
    #`cd Adafruit-Motor-HAT-Python-Library/examples/ && python DualStepperTest.py`
  end
end
