require 'application_responder'
class ApplicationController < ActionController::Base
  self.responder = ApplicationResponder
  respond_to :html
  protect_from_forgery with: :exception

  rescue_from ActiveRecord::RecordNotFound do |execption|
    flash[:error] = "Error 404: File Not Found"
    redirect_to root_path
  end

end
