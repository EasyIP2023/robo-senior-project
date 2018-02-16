class HomeController < ApplicationController

  def index
    # @uploader = Recognize.find(1)
    # @uploader = Recognize.new
    # File.open('/home/vince/Downloads/you_owe_me.mp4') do |f|
    #   @uploader.attachment = f
    # end
    # @uploader.save!
  end

  def push_button
    ExecuteWorker.perform_async
    redirect :back, notice: "Button pushed, Bitch!!"
  end
end
