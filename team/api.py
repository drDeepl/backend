from typing import List

from django.shortcuts import get_object_or_404
from ninja_extra import ControllerBase, api_controller, http_put, permissions, status, http_delete, http_post, http_get, \
    pagination
from ninja_extra.controllers import Detail
from ninja_jwt.authentication import JWTAuth
from ninja.pagination import paginate

from team.models import Team
from team.schemas import CreateTeamSchema, TeamOutSchema, PlayerTeamSchema
from user.models import User
from user.schemas import UserOut
from user.utils import check_admin


@api_controller('/', tags=['Team'], permissions=[permissions.IsAuthenticated], auth=JWTAuth())
class TeamController(ControllerBase):
    @http_get('teams', response=List[TeamOutSchema])
    @paginate
    def get_teams(self):
        qs = [ i for i in Team.objects.all()]
                
        return qs

    @http_get('teams/{team_id}', response=TeamOutSchema)
    def get_team(self, team_id: int):
        team = get_object_or_404(Team, id=team_id)
        return team

    @http_get('teams/{team_id}/participants', response=List[UserOut])
    def get_participants(self, team_id: int):
        team = get_object_or_404(Team, id=team_id)
        participants = User.objects.filter(team=team)
        user: User = self.context.request.auth
        if not user.team == team:
            check_admin(self.context)
        return participants

    @http_post('teams/', response=TeamOutSchema)
    def create_team(self, payload: CreateTeamSchema):
        check_admin(self.context)
        return Team.create(name=payload.name, start_balance=payload.balance)

    @http_put('teams/{team_id}/{name}', response=TeamOutSchema)
    def rename_team(self, team_id: int, name: str):
        check_admin(self.context)
        team = get_object_or_404(Team, id=team_id)
        team.rename(name.replace('\n', '').replace('\t', ''))
        return team

    @http_delete('teams/{team_id}')
    def remove_team(self, team_id: int):
        check_admin(self.context)
        team = get_object_or_404(Team, id=team_id)
        team.delete()
        return {"success": True}

    @http_delete('teams-delete/{flag}')
    def remove_teams(self, flag: int):
        check_admin(self.context)
        
        if(flag):
            teams = Team.objects.all()
            print(teams)
            for team in teams:
                team.delete()
            return {"success": True}
        else:
            return {"success": False}

    @http_put('teams/', response=Detail(status_code=status.HTTP_204_NO_CONTENT))
    def move_player(self, payload: PlayerTeamSchema):
        check_admin(self.context)
        player = get_object_or_404(User, payload.player_id)
        team = get_object_or_404(Team, payload.team_id)
        player.team = team
        player.save()
