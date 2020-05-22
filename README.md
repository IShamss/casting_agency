# Casting Agency API

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

This api has information about movies and actors that you can use for your own applications, It offers a wide variety of information including actors ages and movie release dates

## Authorization

There are 3 types of users that are authorized to use this api, The list below shows these users in addition to their roles:

1)Casting Assistant:
->Can view actors and movies

2)Casting Director:
->All permissions a Casting Assistant has and…
->Add or delete an actor from the database
->Modify actors or movies

3)Executive Producer:
->All permissions a Casting Director has and…
->Add or delete a movie from the database

## End Points and their responses

### Movies Routes

-> GET '/movies' :
{
'success': True,
'movies': all_movies,
}

-> POST '/movies' :
{
'success': True,
'created_movie_id': new_movie.id,
'created_movie_title':new_movie.title
}
Note: your request should include the title and releases_date as strings

-> PATCH '/movies/(movie_id)' :
{
'success': True,
'updated_movie_title':new_title
}
Note: your request should include the title and releases_date as strings

-> DELETE '/movies/(movie_id)' :
{
'success': True,
'deleted':movie_id
}

### Actors Routes

-> GET '/actors' :
{
'success': True,
'actors':all_actors
}

-> POST '/actors' :
{
'success': True,
'created_actor_id': actor.id,
'created_actor_name':new_name
}

-> PATCH '/actors/(actor_id)' :
{
'success': True,
'updated_actor_name':actor.name
}

-> DELETE '/actors/(actor_id)' :
{
'success': True,
'deleted':actor_id
}

## Login & Authentication

https://ishams.auth0.com/authorize?audience=capstoneproj&response_type=token&client_id=MYfcBWBL1mTkNxjjqWWoR4mmTfesYJVk

## Logout

https://ishams.auth0.com/v2/logout?
client_id=MYfcBWBL1mTkNxjjqWWoR4mmTfesYJVk

## Deployed link

https://icasting-agency.herokuapp.com/
