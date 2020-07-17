<?php

namespace Tests\Feature;

use App\Project;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithFaker;
use Tests\TestCase;

class ManageProjectsTest extends TestCase
{
    use RefreshDatabase;
    /**
     * A basic feature test example.
     *
     * @return void
     */
    public function testExample()
    {
        $response = $this->get('/');

        $response->assertStatus(200);
    }

    /** @test */
    public function anyone_can_see_all_projects()
    {
        $project = factory(Project::class)->create();
        $response = $this->get(route("project.index"));

        $response->assertStatus(200);
        $response->assertSee($project->name);

        //should work
    }
    /** @test */
    public function failedTest()
    {

        //bull shit
        $this->assert(false);
    }
}
