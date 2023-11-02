#pragma once

#include <userver/components/component_list.hpp>
#include <userver/storages/postgres/component.hpp>

#include <api/auth_service/v1/auth_service_client.usrv.pb.hpp>
#include <api/auth_service/v1/auth_service_service.usrv.pb.hpp>

#include <string>
#include <string_view>

#include "auth_client.hpp"

namespace auth_service
{

class Auth final : public api::auth_service::v1::AuthServiceBase::Component
{
public:
    static constexpr std::string_view kName = "handler-auth";

    Auth(const userver::components::ComponentConfig& config, const userver::components::ComponentContext& component_context);

    void Register(api::auth_service::v1::AuthServiceBase::RegisterCall& call,
                  api::auth_service::v1::RegisterRequest&&              request) override;
    void Login(api::auth_service::v1::AuthServiceBase::LoginCall& call,
               api::auth_service::v1::LoginRequest&&              request) override;

private:
    userver::storages::postgres::ClusterPtr pg_cluster_;
    AuthClient&                             client_;
};

void AppendAuth(userver::components::ComponentList& component_list);

} // namespace auth_service
